# Background AutoClicker

Un autoclicker avanzado hecho en Python que funciona en segundo plano, permitiéndote usar tu PC mientras farmeas.

![Icon](https://i.imgur.com/your-icon-placeholder.png)

## Características

-   **Segundo Plano (Background)**: Envía clicks directamente a la ventana de Minecraft. ¡Puedes minimizar o hacer Alt+Tab!
-   **Indetectable**: Opción de intervalo aleatorio (Humanización) para evitar bans.
-   **System Tray**: Se minimiza a la bandeja del sistema para no molestar.
-   **Configurable**: Guarda tus preferencias (intervalo, tipo de click) automáticamente.
-   **Feedback Auditivo**: Sonidos al activar/desactivar.
-   **Ligero**: Interfaz simple hecha con Tkinter.

## Cómo usar

1.  Descarga el ejecutable desde la carpeta `dist` o [Releases](#).
2.  Abre Minecraft.
3.  Abre `MinecraftAutoClicker.exe`.
4.  Espera a que diga **Objetivo: Minecraft ...** en verde.
5.  Configura tu intervalo (ej: 1.5s).
6.  **Teclas**:
    -   **F6**: Iniciar / Parar
    -   **F7**: Ocultar Ventana / Mostrar

## Instalación (Código Fuente)

Si prefieres ejecutarlo desde Python:

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/minecraft-autoclicker.git

# 2. Ejecutar el script de instalación (Windows)
setup.bat

# 3. Iniciar
run.bat
```

## Tecnologías

-   Python 3
-   `tkinter` (GUI)
-   `pywin32` (Windows API hooks)
-   `pystray` (System Tray)
-   `pynput` (Teclado)

## Licencia

MIT

