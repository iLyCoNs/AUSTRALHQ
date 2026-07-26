/**
 * ════════════════════════════════════════════════════════════════
 *  OfficeScene.js — AustralDrone.CL Virtual Office
 *  Escena principal de Phaser 3. Carga assets, instancia el CEO,
 *  define hotspots, configura cámara y conecta con n8n webhooks.
 *
 *  FLUJO:
 *    preload() → carga office_map.png + CEO.png + sprite_config_ceo.json
 *    create()  → mundo, sprite sheet, CEO, hotspots, cámara, HUD
 *    update()  → input, movimiento, detección de zonas
 * ════════════════════════════════════════════════════════════════
 */
'use strict';

class OfficeScene extends Phaser.Scene {

    constructor() {
        super({ key: 'OfficeScene' });

        // Dimensiones del mundo (actualizadas al cargar el mapa)
        this.MAP_W = 1920;
        this.MAP_H = 1080;

        // Controladores
        this.ceo      = null;   // CEOController
        this.hotspots = null;   // HotspotManager

        // Input
        this.cursors  = null;
        this.wasd     = null;
        this.shift    = null;

        // Física estática (paredes + obstáculos)
        this.wallGroup = null;

        // Config del avatar
        this.spriteConfig = null;

        // HUD refs
        this._hudState    = null;
        this._hudPos      = null;
        this._hudControls = null;
        this._hudZoom     = null;
    }

    // ══════════════════════════════════════════════════════════════
    //  1. PRELOAD — Carga de assets
    // ══════════════════════════════════════════════════════════════

    preload() {
        // ── Barra de carga ──
        this._createLoadBar();

        // ── MAPA de fondo ──
        // office_map.png debe estar en la raíz del proyecto
        this.load.image('officeMap', 'office_map.png');

        // ── JSON de configuración del sprite sheet ──
        this.load.json('ceoConfig', 'sprites/sprite_config_ceo.json');

        // ── CEO sprite sheet ──
        // Se carga como imagen plana primero; se convierte a spritesheet
        // en create() usando las dimensiones calculadas desde el JSON.
        this.load.image('ceoSheet', 'sprites/CEO.png');

        // ── (Opcional) Efectos de sonido ──
        // this.load.audio('sfx_work',      'audio/keyboard.mp3');
        // this.load.audio('sfx_celebrate', 'audio/fanfare.mp3');

        this.load.on('complete', () => {
            console.log('[OfficeScene] ✅ Assets cargados correctamente.');
        });
    }

    // ══════════════════════════════════════════════════════════════
    //  2. CREATE — Construcción de la escena
    // ══════════════════════════════════════════════════════════════

    create() {
        // 2.0 Leer JSON de configuración del CEO
        this.spriteConfig = this.cache.json.get('ceoConfig');

        // 2.1 Mundo y mapa de fondo
        this._setupWorld();

        // 2.2 Convertir imagen cargada → SpriteSheet de Phaser
        this._buildSpriteSheet();

        // 2.3 Instanciar CEO (posición: escritorio principal)
        this._createCEO(400, 300);

        // 2.4 Input (teclado)
        this._setupInput();

        // 2.5 Hotspots de interacción en el mapa
        this._setupHotspots();

        // 2.6 Cámara que sigue al CEO
        this._setupCamera();

        // 2.7 HUD / UI overlay
        this._setupHUD();

        // 2.8 Conectar con el sistema de webhooks externo (n8n)
        this._connectWebhooks();

        // 2.9 Ajuste al redimensionar ventana
        this.scale.on('resize', this._onResize, this);

        console.log('[OfficeScene] 🎮 Escena lista.');
    }

    // ══════════════════════════════════════════════════════════════
    //  3. UPDATE — Loop de juego
    // ══════════════════════════════════════════════════════════════

    update(time, delta) {
        if (!this.ceo?.sprite) return;

        // 3.1 Procesar input del teclado → mover CEO
        const sprinting = this.shift?.isDown ?? false;
        this.ceo.update(this.cursors, this.wasd, sprinting);

        // 3.2 Verificar hotspots cada frame
        this.hotspots.check(this.ceo.sprite);

        // 3.3 Actualizar HUD
        this._updateHUD();
    }

    // ══════════════════════════════════════════════════════════════
    //  PRIVADOS — Setup
    // ══════════════════════════════════════════════════════════════

    /** Coloca el mapa de fondo y define los límites del mundo. */
    _setupWorld() {
        // Mapa estático de fondo
        const map = this.add.image(0, 0, 'officeMap').setOrigin(0, 0).setDepth(0);

        // Actualizar dimensiones según la imagen real
        this.MAP_W = map.width;
        this.MAP_H = map.height;
        console.log(`[OfficeScene] Mapa: ${this.MAP_W}×${this.MAP_H}px`);

        // Límites del mundo de física (el CEO no puede salir)
        this.physics.world.setBounds(0, 0, this.MAP_W, this.MAP_H);

        // Crear grupo de colisiones estáticas (paredes + mobiliario)
        this._buildCollisionWalls();
    }

    /**
     * Paredes invisibles y obstáculos según el layout del mapa.
     * ⚠️  AJUSTA las coordenadas a tu office_map.png real.
     *
     * Formato: [cx, cy, width, height, label]
     * (cx,cy = centro del rectángulo)
     */
    _buildCollisionWalls() {
        this.wallGroup = this.physics.add.staticGroup();

        const walls = [
            // ── Bordes perimetrales ──
            [this.MAP_W / 2,  36,           this.MAP_W, 72,  'wall-top'],
            [this.MAP_W / 2,  this.MAP_H - 36, this.MAP_W, 72, 'wall-bottom'],
            [36,              this.MAP_H / 2, 72, this.MAP_H, 'wall-left'],
            [this.MAP_W - 36, this.MAP_H / 2, 72, this.MAP_H, 'wall-right'],

            // ── Zona de oficina del CEO Jaime (top-left) ──
            [170, 140, 300, 16, 'boss-jaime-desk-front'],

            // ── Zona de oficina de Nicole (top-right) ──
            [this.MAP_W - 200, 140, 300, 16, 'boss-nicole-desk-front'],

            // ── Mesa central de estrategia ──
            [710, 305, 340, 120, 'strategy-table'],

            // ── Estación de drones (top-right area) ──
            [1145, 200, 250, 90, 'drone-station'],

            // ── Servidores n8n (bottom-left) ──
            [170, 460, 200, 100, 'n8n-servers'],
        ];

        walls.forEach(([cx, cy, w, h, label]) => {
            // Rectángulo invisible — fillAlpha 0 = invisible en producción
            const rect = this.add.rectangle(cx, cy, w, h, 0xff0000, 0);
            this.physics.add.existing(rect, true); // true = estático
            this.wallGroup.add(rect);
        });

        console.log(`[OfficeScene] ${walls.length} zonas de colisión creadas.`);
    }

    /**
     * Convierte la imagen 'ceoSheet' en una textura de spritesheet
     * de Phaser usando las dimensiones calculadas desde el JSON.
     *
     * Esto permite usar generateFrameNumbers() en las animaciones.
     */
    _buildSpriteSheet() {
        const cfg    = this.spriteConfig;
        const src    = this.textures.get('ceoSheet').source[0];
        const frameW = Math.floor(src.width  / (cfg.meta.maxCols   || 12));
        const frameH = Math.floor(src.height / (cfg.meta.totalRows || 4));

        // Agregar como spritesheet al TextureManager de Phaser
        this.textures.addSpriteSheet('ceo', src.image, {
            frameWidth:  frameW,
            frameHeight: frameH,
            margin:      0,
            spacing:     0
        });

        console.log(`[OfficeScene] SpriteSheet 'ceo': ${frameW}×${frameH}px por frame`);
    }

    /**
     * Instancia el CEOController y configura la colisión con las paredes.
     * @param {number} x - Coordenada X inicial en el mundo
     * @param {number} y - Coordenada Y inicial en el mundo
     */
    _createCEO(x, y) {
        this.ceo = new CEOController(this, this.spriteConfig);
        const sprite = this.ceo.create(x, y, this.MAP_W, this.MAP_H);

        // Colisión CEO vs grupo de paredes
        this.physics.add.collider(sprite, this.wallGroup);

        console.log(`[OfficeScene] CEO instanciado @ (${x}, ${y})`);
    }

    /** Crea cursores de teclado (flechas + WASD + Shift). */
    _setupInput() {
        this.cursors = this.input.keyboard.createCursorKeys();
        this.wasd    = this.input.keyboard.addKeys({
            up:    Phaser.Input.Keyboard.KeyCodes.W,
            down:  Phaser.Input.Keyboard.KeyCodes.S,
            left:  Phaser.Input.Keyboard.KeyCodes.A,
            right: Phaser.Input.Keyboard.KeyCodes.D
        });
        this.shift = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT);

        // Tecla [R] = reset CEO al escritorio principal
        this.input.keyboard.on('keydown-R', () => {
            this.ceo.goIdle();
            this.ceo.moveTo(400, 300);
        });

        // Zoom con rueda del ratón
        this.input.on('wheel', (ptr, objs, dx, dy) => {
            const z = Phaser.Math.Clamp(
                this.cameras.main.zoom - dy * 0.0008,
                0.4, 2.5
            );
            this.cameras.main.setZoom(z);
        });
    }

    /**
     * Define los hotspots de interacción del mapa.
     * Cada zona tiene:
     *   - Área rectangular (x, y, w, h)
     *   - Prompt visible al entrar ([E] texto)
     *   - Callbacks onEnter / onExit / onActivate
     *
     * ⚠️  Ajusta las coordenadas según tu office_map.png.
     */
    _setupHotspots() {
        // DEBUG=true muestra bordes de las zonas (quitar en producción)
        const DEBUG = true;

        this.hotspots = new HotspotManager(this);
        this.hotspots.create(DEBUG);

        // ─────────────────────────────────────────────────────────
        //  HOTSPOT 1: Mesa de Estrategia 360°
        //  → Animación Work + notificación al sistema
        // ─────────────────────────────────────────────────────────
        this.hotspots.addHotspot({
            id:     'strategy-table',
            label:  'Mesa Estrategia 360°',
            x: 710, y: 340,
            width: 320, height: 110,
            prompt: '[E] Analizar MasterPlan 360°',
            debug:  DEBUG,
            onEnter: () => {
                this._sysSpeak(7, '📋 Cerca de la Mesa de Estrategia...');
            },
            onActivate: () => {
                // Activar animación Work por 10 segundos
                this.ceo.startWork(10000);

                // Partículas celebración en el mapa
                this._emitParticles(710, 310, '#66fcf1', 14);

                // Notificar al sistema de canvas (si existe)
                this._sysSpeak(7, '🗺️ Revisando MasterPlan 360° — IA analizando macrolotes...');
                this._sysLog('CEO JAIME', 'Análisis MasterPlan en Mesa Estrategia.', '#fbbf24');

                // Enviar evento a n8n
                this._webhookSend({ action: 'scraping_active', location: 'strategy-table' });
            },
            onExit: () => {
                // Si el CEO sale antes de que termine el work, cancelar
                if (this.ceo.state === 'work' && !this.ceo.isBusy) {
                    this.ceo.goIdle();
                }
            }
        });

        // ─────────────────────────────────────────────────────────
        //  HOTSPOT 2: Departamento Legal
        //  → Animación Work (consulta normativa)
        // ─────────────────────────────────────────────────────────
        this.hotspots.addHotspot({
            id:     'legal-corner',
            label:  'Depto. Legal SAG/LGUC',
            x: 170, y: 230,
            width: 200, height: 100,
            prompt: '[E] Consultar normativa SAG/LGUC',
            debug:  DEBUG,
            onActivate: () => {
                this.ceo.startWork(8000);
                this._sysSpeak(7, '⚖️ Revisando DL 3516 SAG y Art.55 LGUC...');
                this._sysLog('CEO JAIME', 'Consultando normativa con Abogado Legal.', '#a855f7');
                this._webhookSend({ action: 'legal_query', location: 'legal-corner' });
            }
        });

        // ─────────────────────────────────────────────────────────
        //  HOTSPOT 3: Taller de Drones
        //  → Animación Work (revisión de flota)
        // ─────────────────────────────────────────────────────────
        this.hotspots.addHotspot({
            id:     'drone-station',
            label:  'Taller Drones 4K',
            x: this.MAP_W - 210, y: 230,
            width: 250, height: 110,
            prompt: '[E] Revisar flota de drones 4K',
            debug:  DEBUG,
            onActivate: () => {
                this.ceo.startWork(6000);
                this._sysSpeak(7, '🚁 Revisando flota de drones 4K para el MasterPlan...');
                this._webhookSend({ action: 'webhook_received', location: 'drone-station' });
            }
        });

        // ─────────────────────────────────────────────────────────
        //  HOTSPOT 4: Cafetería
        //  → Pausa / descanso
        // ─────────────────────────────────────────────────────────
        this.hotspots.addHotspot({
            id:     'cafeteria',
            label:  'Cafetería & Lounge',
            x: this.MAP_W - 185, y: 460,
            width: 260, height: 130,
            prompt: '[E] Tomar un café ☕',
            debug:  DEBUG,
            onEnter: () => {
                this._sysSpeak(7, '☕ La IA no descansa, pero el CEO sí...');
            },
            onActivate: () => {
                this._sysSpeak(7, '☕ ¡Recargando energía para el próximo lead!');
            }
        });

        // ─────────────────────────────────────────────────────────
        //  HOTSPOT 5: Servidores n8n
        //  → Trigger webhook directo
        // ─────────────────────────────────────────────────────────
        this.hotspots.addHotspot({
            id:     'n8n-servers',
            label:  'Servidores n8n',
            x: 170, y: 480,
            width: 200, height: 120,
            prompt: '[E] Monitorear workflows n8n',
            debug:  DEBUG,
            onActivate: () => {
                this.ceo.startWork(5000);
                this._sysSpeak(5, '⚡ CEO revisando workflows de n8n en localhost:5678...');
                this._webhookSend({ action: 'webhook_received', location: 'n8n-servers' });
            }
        });

        // ─────────────────────────────────────────────────────────
        //  HOTSPOT 6: Escritorio del propio CEO Jaime
        //  → Área de retorno seguro
        // ─────────────────────────────────────────────────────────
        this.hotspots.addHotspot({
            id:     'ceo-desk',
            label:  'Escritorio CEO',
            x: 330, y: 145,
            width: 180, height: 80,
            prompt: '[E] Revisar dashboard de leads',
            debug:  DEBUG,
            onActivate: () => {
                this.ceo.startWork(8000);
                this._sysSpeak(7, '📊 Revisando dashboard: 232 leads, 17 grupos FB activos.');
                this._webhookSend({ action: 'scraping_active', location: 'ceo-desk' });
            }
        });

        console.log('[OfficeScene] Hotspots configurados: 6 zonas activas.');
    }

    /** Configura la cámara para seguir al CEO con lerp suave. */
    _setupCamera() {
        const cam = this.cameras.main;
        cam.setBounds(0, 0, this.MAP_W, this.MAP_H);
        cam.startFollow(
            this.ceo.sprite,
            true,  // round pixels (evita blur)
            0.09,  // lerp X (0=rígido, 1=instantáneo)
            0.09   // lerp Y
        );
        cam.setZoom(1.0);
        cam.setDeadzone(80, 60); // Zona muerta central (el CEO puede moverse sin mover la cámara)
        console.log('[OfficeScene] Cámara configurada con seguimiento lerp.');
    }

    /** Crea el HUD fijo sobre la cámara. */
    _setupHUD() {
        const style = {
            fontFamily:      '"Press Start 2P"',
            fontSize:        '7px',
            backgroundColor: '#000000cc',
            padding:         { x: 8, y: 5 }
        };

        // Estado actual del CEO
        this._hudState = this.add.text(14, 14, 'CEO: IDLE', {
            ...style, color: '#66fcf1'
        }).setScrollFactor(0).setDepth(200);

        // Instrucciones de control
        this._hudControls = this.add.text(14, 48, [
            'WASD / ↑↓←→  Mover',
            'Clic derecho  Ir a punto',
            '[E]           Interactuar',
            '[Shift]       Sprint',
            '[R]           Volver al escritorio',
            'Scroll        Zoom'
        ].join('  |  '), {
            ...style,
            fontSize: '4.5px',
            color:    '#475569'
        }).setScrollFactor(0).setDepth(200);

        // Posición del CEO (debug)
        this._hudPos = this.add.text(
            14,
            this.scale.height - 28,
            '',
            { ...style, fontSize: '5px', color: '#334155' }
        ).setScrollFactor(0).setDepth(200);

        // Indicador de zoom
        this._hudZoom = this.add.text(
            this.scale.width - 14,
            14,
            '',
            { ...style, fontSize: '5.5px', color: '#475569' }
        ).setOrigin(1, 0).setScrollFactor(0).setDepth(200);
    }

    /** Actualiza textos del HUD cada frame. */
    _updateHUD() {
        if (!this.ceo) return;

        const state = this.ceo.state.toUpperCase();
        const col   = { IDLE: '#66fcf1', WALK: '#fbbf24', WORK: '#f97316', CELEBRATE: '#10b981' }[state] || '#fff';

        this._hudState.setText(`CEO: ${state}`).setStyle({ color: col });
        this._hudPos.setText(
            `X:${Math.round(this.ceo.x)}  Y:${Math.round(this.ceo.y)}  |  ` +
            (this.hotspots.active ? `📍 ${this.hotspots.active.label}` : '')
        );
        this._hudZoom.setText(`🔍 ${this.cameras.main.zoom.toFixed(2)}×`);
    }

    // ══════════════════════════════════════════════════════════════
    //  INTEGRACIÓN DE WEBHOOKS
    // ══════════════════════════════════════════════════════════════

    /**
     * Conecta con el AvatarWebhookController del sistema anterior (si existe)
     * y expone window.changePhaserCEOState() para disparar estados desde n8n.
     *
     * EVENTOS SOPORTADOS:
     *   { action: 'idle'            }         → CEO va a Idle
     *   { action: 'scraping_active' }         → CEO a Work 10s
     *   { action: 'lead_qualified'  }         → CEO Celebrate
     *   { action: 'moving', destination:'x,y'} → CEO se mueve a ese punto
     */
    _connectWebhooks() {
        // Exponer función global para llamar desde consola o sistema externo
        window.changePhaserCEOState = (event) => {
            if (!this.ceo) return;
            switch (event.action) {
                case 'moving': {
                    const [dx, dy] = (event.destination || '400,300').split(',').map(Number);
                    if (!isNaN(dx) && !isNaN(dy)) this.ceo.moveTo(dx, dy);
                    break;
                }
                case 'scraping_active':
                    this.ceo.startWork(event.duration || 10000);
                    break;
                case 'lead_qualified':
                    this.ceo.startCelebrate();
                    this._emitParticles(this.ceo.x, this.ceo.y, '#fbbf24', 24);
                    break;
                case 'idle':
                    this.ceo.goIdle();
                    break;
                default:
                    console.warn('[OfficeScene] Evento desconocido:', event.action);
            }
        };

        // Si el AvatarWebhookController de la oficina canvas está activo,
        // encadenar su callback para que también controle el Phaser CEO
        if (window._webhookCtrl) {
            const prevOnEvent = window._webhookCtrl.onEvent.bind(window._webhookCtrl);
            window._webhookCtrl.onEvent = (ev) => {
                prevOnEvent(ev);                       // Canvas CEO
                window.changePhaserCEOState(ev);       // Phaser CEO
            };
            console.log('[OfficeScene] Webhook encadenado con _webhookCtrl existente.');
        }

        // Atajo de consola
        window.ceoGo = (action, extra = {}) =>
            window.changePhaserCEOState({ action, ...extra });

        console.log('[OfficeScene] Webhooks listos. Usa: ceoGo("scraping_active") en consola.');
    }

    // ══════════════════════════════════════════════════════════════
    //  HELPERS — Integración con el sistema Canvas anterior
    // ══════════════════════════════════════════════════════════════

    /** Envía burbuja de diálogo si el sistema canvas está disponible. */
    _sysSpeak(agentId, msg) {
        if (typeof speak === 'function') speak(agentId, msg);
        else console.log(`[CEO ${agentId}] ${msg}`);
    }

    /** Agrega línea al log de la bitácora canvas si está disponible. */
    _sysLog(name, msg, color = '#fbbf24') {
        if (typeof log === 'function') log(name, msg, color);
    }

    /** Dispara partículas en el sistema canvas si está disponible. */
    _emitParticles(x, y, color, n = 12) {
        if (typeof spawnP === 'function') spawnP(x, y, color, n);
    }

    /** Envía evento al webhook controller si está activo. */
    _webhookSend(payload) {
        if (window._webhookCtrl) window._webhookCtrl.send(payload);
    }

    // ══════════════════════════════════════════════════════════════
    //  LOADING BAR
    // ══════════════════════════════════════════════════════════════

    _createLoadBar() {
        const W = this.scale.width, H = this.scale.height;
        const bW = 360, bH = 22;
        const bX = W / 2 - bW / 2, bY = H / 2;

        // Fondo oscuro
        this.add.rectangle(W / 2, H / 2, 420, 90, 0x06080f).setDepth(900);

        // Marco de la barra
        const frame = this.add.graphics().setDepth(901);
        frame.lineStyle(2, 0x66fcf1, 0.6);
        frame.strokeRect(bX - 2, bY - 2, bW + 4, bH + 4);

        // Barra de progreso
        const bar = this.add.rectangle(bX, bY, 0, bH, 0x66fcf1).setOrigin(0, 0.5).setDepth(901);

        // Texto
        this.add.text(W / 2, H / 2 - 36, 'AustralDrone.CL — Cargando Oficina...', {
            fontFamily: '"Press Start 2P"',
            fontSize:   '7px',
            color:      '#66fcf1'
        }).setOrigin(0.5).setDepth(902);

        const pct = this.add.text(W / 2, H / 2 + 28, '0%', {
            fontFamily: '"Press Start 2P"',
            fontSize:   '6px',
            color:      '#475569'
        }).setOrigin(0.5).setDepth(902);

        // Actualizar progreso
        this.load.on('progress', (v) => {
            bar.setDisplaySize(bW * v, bH);
            pct.setText(Math.round(v * 100) + '%');
        });

        this.load.on('complete', () => {
            bar.destroy(); frame.destroy(); pct.destroy();
        });
    }

    // ══════════════════════════════════════════════════════════════
    //  RESIZE
    // ══════════════════════════════════════════════════════════════

    _onResize(gameSize) {
        const { width, height } = gameSize;
        if (this._hudPos)   this._hudPos.setY(height - 28);
        if (this._hudZoom)  this._hudZoom.setX(width - 14);
        this.cameras.main.setSize(width, height);
    }
}
