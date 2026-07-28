const { app, BrowserWindow, ipcMain, Tray, Menu } = require('electron');
const path = require('path');
const { fork } = require('child_process');

let mainWindow;
let tray;
let serverProcess;

function startInternalServer() {
    const serverPath = path.join(__dirname, 'server.js');
    console.log('[DESKTOP SUITE] Iniciando servidor agéntico interno:', serverPath);
    
    serverProcess = fork(serverPath, [], {
        cwd: __dirname,
        env: { ...process.env, PORT: '8080', ELECTRON_RUN_AS_NODE: '1' },
        stdio: 'ignore'
    });

    serverProcess.on('error', (err) => {
        console.error('[DESKTOP SUITE ERR] Error en el servidor interno:', err);
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1440,
        height: 920,
        minWidth: 1100,
        minHeight: 700,
        frame: false, // Frameless nativo para estética macOS Glassmorphism
        transparent: true,
        backgroundColor: '#0007090e',
        title: 'AustralHQ Enterprise CRM Suite',
        icon: path.join(__dirname, 'assets', 'icon.ico'),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            webSecurity: false
        }
    });

    // Cargar la aplicación nativa Glassmorphism
    mainWindow.loadFile(path.join(__dirname, 'ENTERPRISE_CRM_APP.html'));

    // Eventos IPC de control de ventana nativa
    ipcMain.on('win-close', () => mainWindow.close());
    ipcMain.on('win-min', () => mainWindow.minimize());
    ipcMain.on('win-max', () => {
        if (mainWindow.isMaximized()) mainWindow.unmaximize();
        else mainWindow.maximize();
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', () => {
    startInternalServer();
    createWindow();
});

app.on('window-all-closed', () => {
    if (serverProcess) serverProcess.kill();
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (mainWindow === null) createWindow();
});
