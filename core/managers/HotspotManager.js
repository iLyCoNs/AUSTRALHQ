/**
 * ════════════════════════════════════════════════════════════════
 *  HotspotManager.js — AustralDrone.CL Virtual Office
 *  Gestiona zonas de interacción invisibles sobre el mapa.
 *  Detecta cuando el CEO entra/sale de un área y permite
 *  activar acciones presionando la tecla [E].
 * ════════════════════════════════════════════════════════════════
 */
'use strict';

class HotspotManager {
    /**
     * @param {Phaser.Scene} scene - Referencia a la escena principal
     */
    constructor(scene) {
        this.scene    = scene;
        this.hotspots = [];        // Array de zonas registradas
        this.active   = null;      // Hotspot donde está el CEO ahora
        this._promptBg   = null;
        this._promptText = null;
        this._actionKey  = null;
        this._debugMode  = false;
    }

    // ──────────────────────────────────────────────────────────────
    //  INICIALIZACIÓN
    // ──────────────────────────────────────────────────────────────

    /**
     * Llama esto en el create() de la escena.
     * @param {boolean} [debug=false] - Muestra borde de zonas visualmente
     */
    create(debug = false) {
        this._debugMode = debug;

        // Tecla de acción (E)
        this._actionKey = this.scene.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.E
        );

        // Crear elementos de la UI del prompt
        this._buildPromptUI();

        console.log('[HotspotManager] ✅ Listo. Tecla de acción: [E]');
    }

    // ──────────────────────────────────────────────────────────────
    //  REGISTRO DE ZONAS
    // ──────────────────────────────────────────────────────────────

    /**
     * Registra una nueva zona de interacción.
     *
     * @param {Object}   cfg
     * @param {string}   cfg.id          - Identificador único
     * @param {string}   cfg.label       - Nombre del área
     * @param {number}   cfg.x           - Centro X del área en el mundo
     * @param {number}   cfg.y           - Centro Y del área en el mundo
     * @param {number}   cfg.width       - Ancho en px
     * @param {number}   cfg.height      - Alto en px
     * @param {string}   cfg.prompt      - Texto del prompt al jugador
     * @param {string}   [cfg.action]    - Animación a disparar ('work'|'celebrate')
     * @param {Function} [cfg.onEnter]   - Callback al entrar al área
     * @param {Function} [cfg.onExit]    - Callback al salir del área
     * @param {Function} [cfg.onActivate]- Callback al presionar [E]
     * @returns {Object} La zona registrada
     */
    addHotspot(cfg) {
        // Zona invisible con física estática
        const zone = this.scene.add.zone(cfg.x, cfg.y, cfg.width, cfg.height);
        zone.setOrigin(0.5);
        this.scene.physics.world.enable(zone, Phaser.Physics.Arcade.STATIC_BODY);

        const hs = {
            id:         cfg.id,
            label:      cfg.label,
            zone,
            action:     cfg.action || 'work',
            prompt:     cfg.prompt || `[E] Interactuar con ${cfg.label}`,
            onEnter:    cfg.onEnter    || null,
            onExit:     cfg.onExit     || null,
            onActivate: cfg.onActivate || null,
            bounds: new Phaser.Geom.Rectangle(
                cfg.x - cfg.width  / 2,
                cfg.y - cfg.height / 2,
                cfg.width,
                cfg.height
            ),
            isOccupied: false
        };

        // Dibujar zona si modo debug
        if (this._debugMode) {
            this._drawDebugZone(cfg);
        }

        this.hotspots.push(hs);
        console.log(`[HotspotManager] Zona registrada: "${cfg.id}" @ (${cfg.x},${cfg.y})`);
        return hs;
    }

    // ──────────────────────────────────────────────────────────────
    //  UPDATE — Llamar desde scene.update()
    // ──────────────────────────────────────────────────────────────

    /**
     * Verifica colisiones y detecta presión de [E].
     * @param {Phaser.Physics.Arcade.Sprite} avatar - Sprite del CEO
     */
    check(avatar) {
        if (!avatar) return;

        const avBounds = avatar.getBounds();
        let found = null;

        // Buscar la primera zona que colisione con el avatar
        for (const hs of this.hotspots) {
            if (Phaser.Geom.Rectangle.Overlaps(avBounds, hs.bounds)) {
                found = hs;
                break;
            }
        }

        // ── Detectar cambio de zona ──
        if (found !== this.active) {
            if (this.active) this._onExit(this.active);
            if (found)       this._onEnter(found);
            this.active = found;
        }

        // ── Tecla [E] presionada mientras está en zona ──
        if (found && Phaser.Input.Keyboard.JustDown(this._actionKey)) {
            this._onActivate(found, avatar);
        }
    }

    // ──────────────────────────────────────────────────────────────
    //  PRIVADOS
    // ──────────────────────────────────────────────────────────────

    _onEnter(hs) {
        hs.isOccupied = true;
        this._showPrompt(hs.prompt, hs.zone.x, hs.zone.y - hs.zone.height / 2 - 20);
        if (hs.onEnter) hs.onEnter(hs);
    }

    _onExit(hs) {
        hs.isOccupied = false;
        this._hidePrompt();
        if (hs.onExit) hs.onExit(hs);
    }

    _onActivate(hs, avatar) {
        console.log(`[HotspotManager] Activado: "${hs.id}"`);
        if (hs.onActivate) hs.onActivate(hs, avatar);
    }

    _buildPromptUI() {
        // Fondo del prompt
        this._promptBg = this.scene.add.graphics();
        this._promptBg.setDepth(150).setScrollFactor(0).setVisible(false);

        // Texto del prompt
        this._promptText = this.scene.add.text(0, 0, '', {
            fontFamily: '"Press Start 2P"',
            fontSize:   '7px',
            color:      '#ffffff'
        });
        this._promptText.setOrigin(0.5, 0.5);
        this._promptText.setDepth(151).setScrollFactor(0).setVisible(false);
    }

    _showPrompt(text, worldX, worldY) {
        // Convertir coordenadas de mundo a pantalla
        const cam = this.scene.cameras.main;
        const sx = (worldX - cam.scrollX) * cam.zoom;
        const sy = (worldY - cam.scrollY) * cam.zoom;

        this._promptText.setText(text);
        this._promptText.setPosition(sx, sy - 40);
        this._promptText.setVisible(true);

        const tw = this._promptText.width + 20;
        const th = this._promptText.height + 12;
        this._promptBg.clear();
        this._promptBg.fillStyle(0x000000, 0.88);
        this._promptBg.fillRoundedRect(sx - tw / 2, sy - 40 - th / 2, tw, th, 4);
        this._promptBg.lineStyle(2, 0x66fcf1, 1);
        this._promptBg.strokeRoundedRect(sx - tw / 2, sy - 40 - th / 2, tw, th, 4);
        this._promptBg.setVisible(true);

        // Pulso de atención
        this.scene.tweens.add({
            targets:  this._promptText,
            alpha:    0.4,
            duration: 550,
            yoyo:     true,
            repeat:   -1,
            ease:     'Sine.easeInOut'
        });
    }

    _hidePrompt() {
        this._promptBg.setVisible(false);
        this._promptText.setVisible(false);
        this.scene.tweens.killTweensOf(this._promptText);
        this._promptText.setAlpha(1);
    }

    _drawDebugZone(cfg) {
        const g = this.scene.add.graphics().setDepth(5);
        g.lineStyle(2, 0x66fcf1, 0.55);
        g.fillStyle(0x66fcf1, 0.05);
        g.fillRect(cfg.x - cfg.width / 2, cfg.y - cfg.height / 2, cfg.width, cfg.height);
        g.strokeRect(cfg.x - cfg.width / 2, cfg.y - cfg.height / 2, cfg.width, cfg.height);

        // Etiqueta de la zona
        this.scene.add.text(cfg.x, cfg.y - cfg.height / 2 - 12, cfg.label, {
            fontFamily: '"Press Start 2P"',
            fontSize:   '5px',
            color:      '#66fcf1',
            alpha:       0.65
        }).setOrigin(0.5, 1).setDepth(6);
    }
}
