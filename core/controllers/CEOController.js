/**
 * ════════════════════════════════════════════════════════════════
 *  CEOController.js — AustralDrone.CL Virtual Office
 *  Controla al avatar del CEO: movimiento, física, animaciones
 *  y máquina de estados integrada con los webhooks de n8n.
 *
 *  ESTADOS: idle → walk → work (10s auto-return) → celebrate → idle
 *
 *  CONTROLES:
 *    Teclado : WASD / Flechas → movimiento directo
 *    Clic    : Click izquierdo en el mapa → movimiento por tween
 *    [Shift] : Sprint (velocidad x1.75)
 *    [E]     : Interactuar con hotspot (gestionado por HotspotManager)
 * ════════════════════════════════════════════════════════════════
 */
'use strict';

class CEOController {
    /**
     * @param {Phaser.Scene} scene        - Escena principal de Phaser
     * @param {Object}       spriteConfig - Objeto JSON de sprite_config_ceo.json
     */
    constructor(scene, spriteConfig) {
        this.scene        = scene;
        this.cfg          = spriteConfig;

        // ── Sprite y física ──
        this.sprite       = null;     // Phaser.Physics.Arcade.Sprite
        this._nameTag     = null;     // Text flotante sobre el CEO

        // ── Estado de movimiento ──
        this.state        = 'idle';   // idle | walk | work | celebrate
        this.isBusy       = false;    // true = work/celebrate en curso → bloquea input
        this.facingRight  = true;

        // ── Velocidades (px/s) ──
        this.speedWalk    = 160;
        this.speedSprint  = 280;
        this._currentSpeed = 160;

        // ── Click-to-move ──
        this._clickTarget = null;     // { x, y } destino del clic
        this._clickTween  = null;     // Tween activo de movimiento
        this._clickFx     = null;     // Indicador visual del clic

        // ── Timers ──
        this._workTimer   = null;

        // ── Dimensiones del frame (calculadas en create) ──
        this.frameW       = 64;
        this.frameH       = 64;
    }

    // ══════════════════════════════════════════════════════════════
    //  INICIALIZACIÓN — llamar desde OfficeScene.create()
    // ══════════════════════════════════════════════════════════════

    /**
     * Crea el sprite del CEO con física y lo posiciona en el mapa.
     *
     * @param {number} startX    - X inicial (en coordenadas de mundo)
     * @param {number} startY    - Y inicial
     * @param {number} worldW    - Ancho del mundo (para setBoundsCollision)
     * @param {number} worldH    - Alto del mundo
     * @returns {Phaser.Physics.Arcade.Sprite}
     */
    create(startX, startY, worldW, worldH) {
        // Calcular dimensiones de frame desde la textura cargada
        this._computeFrameDimensions();

        // ── Sprite con física arcade ──
        this.sprite = this.scene.physics.add.sprite(startX, startY, 'ceo');
        this.sprite.setDepth(50);
        this.sprite.setCollideWorldBounds(true);

        // Escalar sprite al doble para visibilidad en el mapa
        this.sprite.setDisplaySize(this.frameW * 2, this.frameH * 2);

        // Hitbox reducido al 50% del frame, anclado en los pies
        this.sprite.body.setSize(this.frameW * 0.55, this.frameH * 0.45);
        this.sprite.body.setOffset(
            this.frameW * 0.225,
            this.frameH * 0.55
        );

        // ── Crear todas las animaciones desde el JSON ──
        this._buildAnimations();

        // ── UI: nametag flotante ──
        this._buildNameTag();

        // ── UI: indicador de clic en el suelo ──
        this._buildClickIndicator();

        // ── Input: clic para mover ──
        this.scene.input.on('pointerdown', (ptr) => {
            if (ptr.leftButtonDown() && !this.isBusy) {
                this.moveTo(ptr.worldX, ptr.worldY);
            }
        });

        // Iniciar en Idle
        this.play('idle');

        console.log(`[CEOController] ✅ CEO creado @ (${startX},${startY}) | frame: ${this.frameW}×${this.frameH}px`);
        return this.sprite;
    }

    // ══════════════════════════════════════════════════════════════
    //  UPDATE — llamar desde OfficeScene.update()
    // ══════════════════════════════════════════════════════════════

    /**
     * Procesa input de teclado y actualiza el estado cada frame.
     * @param {Phaser.Types.Input.Keyboard.CursorKeys} cursors - Teclas de flecha
     * @param {Object} wasd    - { up, down, left, right }
     * @param {boolean} sprint - true si Shift está presionado
     */
    update(cursors, wasd, sprint = false) {
        if (!this.sprite) return;

        // Actualizar nametag a la posición del sprite
        this._syncNameTag();

        // Bloqueo durante work/celebrate
        if (this.isBusy) {
            this.sprite.body.setVelocity(0, 0);
            return;
        }

        this._currentSpeed = sprint ? this.speedSprint : this.speedWalk;

        // ── Calcular vector de velocidad desde teclado ──
        let vx = 0, vy = 0;
        const s = this._currentSpeed;

        if (cursors.left.isDown  || wasd.left.isDown)  vx = -s;
        else if (cursors.right.isDown || wasd.right.isDown) vx = s;
        if (cursors.up.isDown    || wasd.up.isDown)    vy = -s;
        else if (cursors.down.isDown  || wasd.down.isDown)  vy = s;

        const keyboardActive = vx !== 0 || vy !== 0;

        if (keyboardActive) {
            // Si el usuario teclea, cancelar click-to-move
            this._cancelClickMove();

            // Normalizar diagonal (evitar velocidad mayor en 45°)
            if (vx !== 0 && vy !== 0) {
                vx *= 0.7071;
                vy *= 0.7071;
            }

            this.sprite.body.setVelocity(vx, vy);
            this._setFacing(vx);
            if (this.state !== 'walk') this.play('walk');

        } else if (!this._clickTarget) {
            // Sin teclado y sin click-to-move activo → detenerse
            this.sprite.body.setVelocity(0, 0);
            if (this.state === 'walk') this.play('idle');
        }
        // Si hay _clickTarget activo, el tween maneja la posición
    }

    // ══════════════════════════════════════════════════════════════
    //  ACCIONES PÚBLICAS
    // ══════════════════════════════════════════════════════════════

    /**
     * Mueve al CEO hacia las coordenadas de mundo (x, y).
     * Utiliza un Tween de Phaser para movimiento suave.
     * La animación Walk se activa automáticamente.
     *
     * @param {number} tx - Target X (mundo)
     * @param {number} ty - Target Y (mundo)
     */
    moveTo(tx, ty) {
        if (this.isBusy) return;

        // Cancelar movimiento anterior si existe
        this._cancelClickMove();

        this._clickTarget = { x: tx, y: ty };
        this._showClickIndicator(tx, ty);

        // Calcular duración según distancia y velocidad
        const dist     = Phaser.Math.Distance.Between(this.sprite.x, this.sprite.y, tx, ty);
        const duration = Math.max((dist / this._currentSpeed) * 1000, 80);

        // Orientar sprite
        this._setFacing(tx - this.sprite.x);
        this.play('walk');

        // Tween de posición
        this._clickTween = this.scene.tweens.add({
            targets:  this.sprite,
            x:        tx,
            y:        ty,
            duration,
            ease:     'Linear',
            onUpdate: () => {
                // Actualizar cuerpo de física manualmente (el tween bypasea la física)
                if (this.sprite.body) {
                    this.sprite.body.reset(this.sprite.x, this.sprite.y);
                }
            },
            onComplete: () => {
                this._clickTarget = null;
                this._clickTween  = null;
                this._hideClickIndicator();
                if (!this.isBusy) this.play('idle');
            }
        });
    }

    /**
     * Activa la animación Work (scraping/análisis activo).
     * Vuelve automáticamente a Idle después de [duration] ms.
     *
     * @param {number} [duration=10000] - Tiempo en ms (default 10s por n8n config)
     */
    startWork(duration = 10000) {
        if (this.isBusy && this.state === 'celebrate') return; // celebrate tiene prioridad

        this._cancelClickMove();
        this.sprite.body.setVelocity(0, 0);
        this.isBusy = true;
        this.play('work');

        clearTimeout(this._workTimer);
        this._workTimer = setTimeout(() => {
            this.isBusy = false;
            this.play('idle');
            console.log('[CEOController] Work completo → Idle');
        }, duration);
    }

    /**
     * Activa la animación Celebrate (lead calificado).
     * Vuelve a Idle al completar el ciclo de animación (no-loop).
     */
    startCelebrate() {
        this._cancelClickMove();
        clearTimeout(this._workTimer);
        this.sprite.body.setVelocity(0, 0);
        this.isBusy = true;
        this.play('celebrate');
        // El retorno a Idle está en el listener 'animationcomplete' dentro de play()
    }

    /**
     * Fuerza el estado Idle y cancela cualquier acción en curso.
     */
    goIdle() {
        this._cancelClickMove();
        clearTimeout(this._workTimer);
        this.isBusy = false;
        this.sprite.body.setVelocity(0, 0);
        this.play('idle');
    }

    /**
     * Cambia la animación activa.
     * @param {string} animName - 'idle' | 'walk' | 'work' | 'celebrate'
     */
    play(animName) {
        if (this.state === animName) return;
        this.state = animName;

        const key = `ceo-${animName}`;
        if (!this.scene.anims.exists(key)) {
            console.warn(`[CEOController] Animación "${key}" no encontrada.`);
            return;
        }

        this.sprite.play(key, true);

        // celebrate: cuando termina el ciclo → volver a idle
        if (animName === 'celebrate') {
            this.sprite.once(Phaser.Animations.Events.ANIMATION_COMPLETE, () => {
                this.isBusy = false;
                this.play('idle');
                console.log('[CEOController] Celebrate completo → Idle');
            });
        }

        console.log(`[CEOController] Anim → "${animName}"`);
    }

    // ══════════════════════════════════════════════════════════════
    //  PROPIEDADES
    // ══════════════════════════════════════════════════════════════

    get x()        { return this.sprite?.x ?? 0; }
    get y()        { return this.sprite?.y ?? 0; }
    get position() { return { x: this.x, y: this.y }; }
    get isMoving() { return this.state === 'walk'; }

    // ══════════════════════════════════════════════════════════════
    //  PRIVADOS
    // ══════════════════════════════════════════════════════════════

    /**
     * Calcula frameW y frameH desde la textura ya cargada + JSON config.
     */
    _computeFrameDimensions() {
        const tex = this.scene.textures.get('ceo');
        if (tex && tex.source[0]) {
            const src = tex.source[0];
            this.frameW = Math.floor(src.width  / (this.cfg.meta.maxCols   || 12));
            this.frameH = Math.floor(src.height / (this.cfg.meta.totalRows || 4));
        }
        console.log(`[CEOController] Frame calculado: ${this.frameW}×${this.frameH}px`);
    }

    /**
     * Genera todas las animaciones de Phaser desde el JSON de configuración.
     * Frames absolutos = row * maxCols + frameIndex
     */
    _buildAnimations() {
        const maxCols = this.cfg.meta.maxCols || 12;
        const anims   = this.cfg.animations   || {};

        Object.entries(anims).forEach(([key, animCfg]) => {
            const phKey = `ceo-${key}`;
            if (this.scene.anims.exists(phKey)) return; // No duplicar

            const startFrame = animCfg.row * maxCols + (animCfg.startFrame || 0);
            const endFrame   = animCfg.row * maxCols + (animCfg.endFrame   || animCfg.frameCount - 1);

            this.scene.anims.create({
                key,
                frames:    this.scene.anims.generateFrameNumbers('ceo', { start: startFrame, end: endFrame }),
                frameRate: animCfg.fps   || 10,
                repeat:    animCfg.loop  ? -1 : 0,
                yoyo:      false
            });

            console.log(`[CEOController] Anim "${phKey}": frames ${startFrame}→${endFrame} @ ${animCfg.fps}fps loop=${animCfg.loop}`);
        });
    }

    /** Crea el texto con el nombre del CEO flotando sobre el sprite. */
    _buildNameTag() {
        this._nameTag = this.scene.add.text(this.x, this.y - 60, '👔 CEO JAIME', {
            fontFamily:      '"Press Start 2P"',
            fontSize:        '6px',
            color:           '#fbbf24',
            backgroundColor: '#000000',
            padding:         { x: 6, y: 3 }
        });
        this._nameTag.setOrigin(0.5, 1).setDepth(52);
    }

    _syncNameTag() {
        if (this._nameTag) {
            this._nameTag.setPosition(
                this.x,
                this.y - (this.frameH * 2) / 2 - 8
            );
        }
    }

    /** Crea el gráfico del indicador de destino de clic. */
    _buildClickIndicator() {
        this._clickFx = this.scene.add.graphics().setDepth(12);
        this._clickFx.setVisible(false);
    }

    _showClickIndicator(x, y) {
        const g = this._clickFx;
        g.clear();
        // Anillo exterior
        g.lineStyle(2, 0x66fcf1, 0.9);
        g.strokeCircle(x, y, 14);
        // Punto central
        g.fillStyle(0x66fcf1, 0.6);
        g.fillCircle(x, y, 4);
        // Cruz cardinal
        g.lineStyle(1, 0x66fcf1, 0.5);
        g.lineBetween(x - 10, y, x - 5, y);
        g.lineBetween(x + 5,  y, x + 10, y);
        g.lineBetween(x, y - 10, x, y - 5);
        g.lineBetween(x, y + 5,  x, y + 10);
        g.setVisible(true);
        g.setAlpha(1);

        // Fade out suave
        this.scene.tweens.add({
            targets:  g,
            alpha:    0,
            duration: 900,
            ease:     'Quad.easeOut',
            onComplete: () => g.setVisible(false).setAlpha(1)
        });
    }

    _hideClickIndicator() {
        if (this._clickFx) {
            this._clickFx.setVisible(false);
            this._clickFx.setAlpha(1);
        }
    }

    _cancelClickMove() {
        if (this._clickTween) {
            this._clickTween.stop();
            this._clickTween = null;
            if (this.sprite?.body) {
                this.sprite.body.reset(this.sprite.x, this.sprite.y);
            }
        }
        this._clickTarget = null;
        this._hideClickIndicator();
    }

    _setFacing(vx) {
        if (!this.sprite) return;
        if (vx > 0)       { this.sprite.setFlipX(false); this.facingRight = true;  }
        else if (vx < 0)  { this.sprite.setFlipX(true);  this.facingRight = false; }
    }
}
