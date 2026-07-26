/**
 * ══════════════════════════════════════════════════════════════════
 *  CEO AVATAR WEBHOOK CONTROLLER — AustralDrone.CL Virtual Office
 *  v2.0.0 — Compatible con n8n WebSocket + HTTP Polling fallback
 *  Autor: AustralDrone.CL Ecosystem
 * ══════════════════════════════════════════════════════════════════
 *
 *  FLUJO DE DATOS:
 *  Python Agents → n8n Webhook → WebSocket/HTTP → changeAvatarState() → Canvas Sprite
 *
 *  USO:
 *  const ctrl = new AvatarWebhookController({ onEvent: changeAvatarState });
 *  ctrl.connect();
 *
 *  TRIGGER MANUAL (consola del navegador):
 *  window.ceoEvent('scraping_active')
 *  window.ceoEvent('lead_qualified', { leadName: 'Carlos Méndez 145 Has' })
 *  window.ceoEvent('moving', { destination: '680,290' })
 * ══════════════════════════════════════════════════════════════════
 */

'use strict';

// ════════════════════════════════════════════
//  CLASS: CEOSpritePlayer
//  Renderiza el sprite sheet CEO.png en canvas
// ════════════════════════════════════════════
class CEOSpritePlayer {
    /**
     * @param {HTMLImageElement} image - CEO.png cargada
     * @param {Object} config - sprite_config_ceo.json parseado
     */
    constructor(image, config) {
        this.image       = image;
        this.config      = config;
        // Auto-detect frame dimensions from image + config
        this.frameWidth  = Math.floor(image.naturalWidth  / config.meta.maxCols);
        this.frameHeight = Math.floor(image.naturalHeight / config.meta.totalRows);
        this.currentAnim = 'idle';
        this.currentFrame = 0;
        this.lastFrameMs  = 0;
        this.workTimer    = null;
        this.loaded       = true;

        console.log(`[CEOSprite] Loaded: ${image.naturalWidth}x${image.naturalHeight}px`);
        console.log(`[CEOSprite] Frame: ${this.frameWidth}x${this.frameHeight}px`);
        console.log(`[CEOSprite] Animations:`, Object.keys(config.animations));
    }

    /** Avanza la animación al siguiente frame según FPS configurado */
    update(ms) {
        const anim = this.config.animations[this.currentAnim];
        if (!anim) return;

        const interval = 1000 / anim.fps;
        if (ms - this.lastFrameMs >= interval) {
            this.currentFrame++;
            if (this.currentFrame >= anim.frameCount) {
                if (anim.loop) {
                    this.currentFrame = 0;
                } else {
                    // Animación no-loop terminó (ej: celebrate)
                    this.currentFrame = anim.frameCount - 1;
                    if (anim.onComplete) {
                        // Retornar a la animación configurada
                        setTimeout(() => this.setAnim(anim.onComplete), 80);
                    }
                }
            }
            this.lastFrameMs = ms;
        }
    }

    /**
     * Cambia la animación activa
     * @param {string} animName - 'idle' | 'walk' | 'work' | 'celebrate'
     */
    setAnim(animName) {
        const anim = this.config.animations[animName];
        if (!anim) {
            console.warn(`[CEOSprite] Animación '${animName}' no encontrada. Usando 'idle'.`);
            animName = 'idle';
        }
        if (this.currentAnim === animName) return; // ya está en esa anim

        this.currentAnim  = animName;
        this.currentFrame = 0;
        this.lastFrameMs  = 0;
        console.log(`[CEOSprite] → Animación: "${animName}" (${anim.frameCount} frames @ ${anim.fps}fps)`);
    }

    /**
     * Dibuja el frame actual en el canvas
     * @param {CanvasRenderingContext2D} ctx
     * @param {number} cx - Center X en canvas
     * @param {number} cy - Feet Y en canvas (sprite dibuja hacia arriba)
     * @param {number} drawH - Alto deseado en canvas px
     */
    draw(ctx, cx, cy, drawH) {
        const anim = this.config.animations[this.currentAnim];
        if (!anim || !this.image) return;

        // Source rect en el sprite sheet
        const sx = this.currentFrame * this.frameWidth;
        const sy = anim.row * this.frameHeight;

        // Mantener aspect ratio
        const aspect = this.frameWidth / this.frameHeight;
        const drawW  = drawH * aspect;

        ctx.drawImage(
            this.image,
            sx, sy, this.frameWidth, this.frameHeight,  // source
            cx - drawW / 2, cy - drawH, drawW, drawH    // dest (feet at cy)
        );
    }

    get animLabel() {
        const anim = this.config.animations[this.currentAnim];
        return `${this.currentAnim.toUpperCase()} [${this.currentFrame+1}/${anim?.frameCount||'?'}]`;
    }
}

// ════════════════════════════════════════════
//  CLASS: AvatarWebhookController
//  WebSocket primario + HTTP Polling fallback
// ════════════════════════════════════════════
class AvatarWebhookController {
    /**
     * @param {Object} options
     * @param {string}   options.wsUrl        WebSocket URL de n8n
     * @param {string}   options.pollUrl      HTTP Polling URL de n8n
     * @param {number}   options.pollInterval Intervalo en ms (default 3000)
     * @param {Function} options.onEvent      Callback(event) cuando llega un evento
     * @param {Function} options.onStatus     Callback(status) cambio de estado de conexión
     */
    constructor(options = {}) {
        this.wsUrl        = options.wsUrl        || 'ws://localhost:5678/webhook-ws/ceo-avatar';
        this.pollUrl      = options.pollUrl       || 'http://localhost:5678/webhook/ceo-avatar-state';
        this.sendUrl      = options.sendUrl       || 'http://localhost:5678/webhook/office-events';
        this.pollInterval = options.pollInterval  || 3000;
        this.onEvent      = options.onEvent       || (() => {});
        this.onStatus     = options.onStatus      || (() => {});

        this.ws            = null;
        this.pollTimer     = null;
        this.reconnTimer   = null;
        this.wsConnected   = false;
        this.status        = 'initializing';
        this._lastEventId  = null;   // deduplication
    }

    /** Inicia WebSocket + Polling en paralelo */
    connect() {
        console.log('[WebhookCtrl] Connecting to n8n...');
        this._connectWS();
        this._startPolling();
    }

    /** Desconecta todo */
    disconnect() {
        if (this.ws)         { this.ws.close(); this.ws = null; }
        if (this.pollTimer)  { clearInterval(this.pollTimer); }
        if (this.reconnTimer){ clearTimeout(this.reconnTimer); }
        this._setStatus('disconnected');
    }

    // ── WEBSOCKET ──
    _connectWS() {
        try {
            this.ws = new WebSocket(this.wsUrl);

            this.ws.onopen = () => {
                this.wsConnected = true;
                this._setStatus('ws-connected');
                console.log('[WebhookCtrl] ✅ WebSocket conectado:', this.wsUrl);
            };

            this.ws.onmessage = (e) => {
                try {
                    const data = JSON.parse(e.data);
                    this._handleEvent(data, 'ws');
                } catch (err) {
                    console.warn('[WebhookCtrl] WS mensaje no-JSON:', e.data);
                }
            };

            this.ws.onclose = (e) => {
                this.wsConnected = false;
                this._setStatus('ws-reconnecting');
                console.log(`[WebhookCtrl] WS cerrado (code ${e.code}). Reconectando en 5s...`);
                this.reconnTimer = setTimeout(() => this._connectWS(), 5000);
            };

            this.ws.onerror = () => {
                this._setStatus('ws-error-polling-active');
                console.warn('[WebhookCtrl] WS error — modo polling activo.');
            };

        } catch (e) {
            this._setStatus('polling-only');
            console.warn('[WebhookCtrl] WebSocket no disponible:', e.message);
        }
    }

    // ── HTTP POLLING ──
    _startPolling() {
        clearInterval(this.pollTimer);
        this.pollTimer = setInterval(async () => {
            // Si WebSocket está activo, el polling es solo de respaldo
            // igual lo ejecutamos para detectar eventos que el WS pudo perder
            try {
                const resp = await fetch(this.pollUrl, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json', 'X-Office-Client': 'australdrone-virtual-office' },
                    signal: AbortSignal.timeout(2500)
                });

                if (resp.ok) {
                    const data = await resp.json();
                    if (!this.wsConnected) this._setStatus('polling-ok');
                    if (data && data.action) this._handleEvent(data, 'poll');
                } else if (!this.wsConnected) {
                    this._setStatus('polling-no-data');
                }
            } catch (err) {
                if (!this.wsConnected) this._setStatus('n8n-offline');
            }
        }, this.pollInterval);
    }

    // ── DEDUPLICATION + DISPATCH ──
    _handleEvent(data, source) {
        // Deduplicar por eventId si existe
        if (data.eventId && data.eventId === this._lastEventId) return;
        this._lastEventId = data.eventId || null;

        console.log(`[WebhookCtrl] 📨 Evento (${source}):`, data);
        this.onEvent(data);
    }

    // ── ENVIAR EVENTO A N8N ──
    /**
     * Envía un evento al webhook de n8n (fire-and-forget)
     * @param {Object} payload - { action, ...data }
     */
    send(payload) {
        const body = {
            ...payload,
            timestamp: new Date().toISOString(),
            source: 'australdrone-virtual-office'
        };
        fetch(this.sendUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        }).catch(() => {}); // fire and forget — no bloquea la UI
        console.log('[WebhookCtrl] → Enviado a n8n:', body);
    }

    _setStatus(s) {
        this.status = s;
        this.onStatus(s);
    }

    get statusLabel() {
        const labels = {
            'initializing':          '⏳ Iniciando...',
            'ws-connected':          '🟢 WebSocket n8n',
            'ws-reconnecting':       '🟡 WS Reconectando...',
            'ws-error-polling-active':'🟡 WS Error | Polling',
            'polling-only':          '🔵 HTTP Polling',
            'polling-ok':            '🔵 HTTP Polling OK',
            'polling-no-data':       '🟡 Polling sin datos',
            'n8n-offline':           '🔴 n8n Offline',
            'disconnected':          '⚫ Desconectado'
        };
        return labels[this.status] || this.status;
    }
}

// ════════════════════════════════════════════
//  FUNCIÓN PRINCIPAL: changeAvatarState(event)
//  Controlador de estados del CEO avatar
// ════════════════════════════════════════════
/**
 * Cambia el estado de animación del CEO según el evento recibido.
 *
 * EVENTOS SOPORTADOS:
 *   { "action": "idle" }                                         → Idle loop
 *   { "action": "moving", "destination": "680,290" }            → Walk + mover a destino
 *   { "action": "scraping_active" }                             → Work 10s → auto-idle
 *   { "action": "lead_qualified", "leadName": "Carlos M." }     → Celebrate → idle
 *
 * @param {Object} event - Payload JSON del webhook n8n
 */
function changeAvatarState(event) {
    if (!window._ceoSprite || !window._spriteConfig) {
        console.warn('[changeAvatarState] Sprite no cargado aún. Evento encolado:', event);
        // Queue para cuando cargue
        window._pendingCEOEvents = window._pendingCEOEvents || [];
        window._pendingCEOEvents.push(event);
        return;
    }

    const sprite    = window._ceoSprite;
    const config    = window._spriteConfig;
    const eventMap  = config.webhookEventMap || {};
    const animName  = eventMap[event.action] || 'idle';

    // 1. Cambiar animación
    sprite.setAnim(animName);

    // 2. Efectos secundarios según acción
    switch (event.action) {

        case 'moving': {
            const dest = event.destination || '';
            const [dxStr, dyStr] = dest.split(',');
            const dx = parseFloat(dxStr), dy = parseFloat(dyStr);
            if (!isNaN(dx) && !isNaN(dy)) {
                // Mover el boss al destino
                if (window.BOSSES && window.BOSSES[0]) {
                    window.BOSSES[0].x = dx;
                    window.BOSSES[0].y = dy;
                }
            }
            if (window.speak) speak(7, `🚶 CEO en camino a [${dest || 'nuevo destino'}]...`);
            break;
        }

        case 'scraping_active': {
            if (window.speak)  speak(7, '💻 ¡Scraping activo! Analizando macrolotes en Los Lagos...');
            if (window.setDot) setDot(7, true);
            clearTimeout(window._ceoWorkTimer);
            window._ceoWorkTimer = setTimeout(() => {
                sprite.setAnim('idle');
                if (window.setDot)  setDot(7, false);
                if (window.speak)   speak(7, '✅ Análisis completado. Revisando resultados.');
                if (window.addLog)  addLog('CEO JAIME', 'Trabajo completado. Volviendo a Idle.', '#fbbf24');
            }, config.animations.work?.autoReturnDelay || 10000);
            break;
        }

        case 'lead_qualified': {
            const leadName = event.leadName || 'Prospecto B2B';
            if (window.speak)   speak(7, `🎉 ¡"${leadName}" calificado! ¡CONVERSIÓN EXITOSA!`);
            if (window.setDot)  setDot(7, true);
            if (window.spawnP)  spawnP(window.BOSSES[0].x, window.BOSSES[0].y, '#fbbf24', 28);
            // También notificar a Nicole
            setTimeout(() => {
                if (window.speak)  speak(8, `🎊 ¡Nicole! ${leadName} convirtió. Reportando métricas.`);
                if (window.spawnP) spawnP(window.BOSSES[1].x, window.BOSSES[1].y, '#ec4899', 18);
                if (window.setDot) setDot(7, false);
            }, 3200);
            break;
        }

        case 'idle':
        default: {
            clearTimeout(window._ceoWorkTimer);
            if (window.setDot) setDot(7, false);
            if (window.speak)  speak(7, '😌 CEO revisando el dashboard de AustralDrone...');
            break;
        }
    }

    // 3. Log en consola de la oficina
    if (window.addLog) {
        addLog(
            `n8n → CEO JAIME`,
            `Evento: "${event.action}" → Anim: "${animName}"`,
            '#fbbf24'
        );
    }

    // 4. Incrementar contador de webhooks
    if (window.incWH) incWH();

    return animName; // útil para testing
}

// ════════════════════════════════════════════
//  EXPORTAR para uso como módulo (Node / ES Module)
// ════════════════════════════════════════════
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CEOSpritePlayer, AvatarWebhookController, changeAvatarState };
}
if (typeof window !== 'undefined') {
    window.CEOSpritePlayer         = CEOSpritePlayer;
    window.AvatarWebhookController = AvatarWebhookController;
    window.changeAvatarState       = changeAvatarState;
}
