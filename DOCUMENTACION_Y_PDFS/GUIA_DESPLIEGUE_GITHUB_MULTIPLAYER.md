# 🌐 GUÍA DE DESPLIEGUE EN VIVO: AUSTRALDRONE HQ MULTIJUGADOR

## 🎯 Resumen Arquitectura
Para que **JAIME (CEO)**, **NICOLE (DIR)** y **DIEGO (SUB)** puedan conectarse simultáneamente desde distintos computadores y verse en tiempo real en la oficina interactiva con chat live, se despliega en 2 partes complementarias:

```
┌────────────────────────────────────────────────────────┐
│ 1. FRONTEND (GitHub Pages / Vercel / Render)          │
│    - Renderiza Phaser 3, Sprites pixel art y UI Chat   │
│    - Accesible públicamente vía HTTPS                  │
└──────────────────────────┬─────────────────────────────┘
                           │ Conexión WebSocket (wss://)
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. BACKEND MULTIPLAYER (Render / Railway / Glitch)      │
│    - Corre `server.js` (Node.js + WebSockets)          │
│    - Sincroniza movimientos, animaciones y mensajes     │
│    - Gratuito 24/7                                     │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Opción A: Despliegue 100% Automático en Render (RECOMENDADO - 5 minutos)

### Paso 1: Subir el proyecto a un Repositorio Público en GitHub
1. Entra a [GitHub.com](https://github.com/new) y crea un nuevo repositorio público llamado **`australdrone-hq`**.
2. Sube todos los archivos del proyecto (incluyendo la carpeta `/sprites/`).

### Paso 2: Crear Web Service Gratuito en Render.com
1. Entra a [Render.com](https://render.com) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **New +** → **Web Service**.
3. Conecta tu repositorio **`australdrone-hq`**.
4. Configura los siguientes campos:
   - **Name**: `australdrone-hq`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `node server.js`
   - **Plan**: `Free`
5. Haz clic en **Create Web Service**. Render te dará un enlace público HTTPS / WSS como:  
   👉 `https://australdrone-hq.onrender.com`

---

## ⚡ Opción B: GitHub Pages + Backend WebSocket

Si deseas que la página cargue directamente desde `https://tu-usuario.github.io/australdrone-hq/`:

1. En tu repositorio de GitHub, ve a **Settings** → **Pages**.
2. En **Source**, selecciona `main` branch y carpeta `/ (root)`.
3. Haz clic en **Save**. En 1 minuto tendrás tu enlace público de GitHub Pages.

---

## 🔑 Acceso para Ejecutivos

Una vez desplegada la URL pública:
1. **Jaime**: Accede a la URL, elige **CEO JAIME** e ingresa su token/pass.
2. **Nicole**: Accede a la URL, elige **DIR. NICOLE** e ingresa su token/pass.
3. **Diego**: Accede a la URL, elige **SUB. DIEGO** e ingresa su token/pass.

¡Cada uno verá la pantalla enfocada en su personaje y observará en tiempo real el movimiento y los globos de chat de los demás ejecutivos en la oficina!
