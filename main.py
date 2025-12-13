import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput import keyboard
import win32gui
import win32api
import win32con
import pystray
from PIL import Image, ImageDraw
import json
import random
import winsound
import os

CONFIG_FILE = "config.json"

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft AutoClicker (Tray)")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.running = False
        self.program_running = True
        self.target_hwnd = None
        self.visible = True
        self.icon = None

        # Variables
        self.interval_var = tk.StringVar(value="1.5")
        self.status_var = tk.StringVar(value="Detenido")
        self.window_status_var = tk.StringVar(value="Buscando Minecraft...")
        self.randomize_var = tk.BooleanVar(value=False)
        self.click_type_var = tk.StringVar(value="Izquierdo")

        # Load Config
        self.load_config()

        # UI Components
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Window Status
        self.window_label = ttk.Label(main_frame, textvariable=self.window_status_var, wraplength=350)
        self.window_label.pack(pady=(0, 10))

        # Interval
        ttk.Label(main_frame, text="Intervalo (segundos):").pack(pady=5)
        self.interval_entry = ttk.Entry(main_frame, textvariable=self.interval_var, width=10)
        self.interval_entry.pack(pady=5)

        # Humanization
        ttk.Checkbutton(main_frame, text="Variación Aleatoria (+/- 10%)", variable=self.randomize_var).pack(pady=5)

        # Click Type
        ttk.Label(main_frame, text="Tipo de Click:").pack(pady=5)
        click_type_combo = ttk.Combobox(main_frame, textvariable=self.click_type_var, values=["Izquierdo", "Derecho"], state="readonly", width=10)
        click_type_combo.pack(pady=5)

        # Status
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Helvetica", 12, "bold"), foreground="red")
        self.status_label.pack(pady=15)

        ttk.Label(main_frame, text="F6: Iniciar/Parar | F7: Ocultar/Mostrar").pack(pady=5, side=tk.BOTTOM)

        # Threads
        self.click_thread = threading.Thread(target=self.clicker_loop)
        self.click_thread.daemon = True
        self.click_thread.start()

        self.window_finder_thread = threading.Thread(target=self.find_minecraft_window)
        self.window_finder_thread.daemon = True
        self.window_finder_thread.start()
        
        # System Tray Setup
        self.setup_tray()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        # Handle X button
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.interval_var.set(config.get("interval", "1.5"))
                    self.randomize_var.set(config.get("randomize", False))
                    self.click_type_var.set(config.get("click_type", "Izquierdo"))
            except Exception:
                pass

    def save_config(self):
        config = {
            "interval": self.interval_var.get(),
            "randomize": self.randomize_var.get(),
            "click_type": self.click_type_var.get()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass

    def setup_tray(self):
        image = self.create_tray_image()
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar", self.show_window_from_tray),
            pystray.MenuItem("Salir", self.quit_app)
        )
        self.icon = pystray.Icon("MinecraftAutoClicker", image, "Minecraft Clicker", menu)
        
        # Run tray icon in separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()

    def create_tray_image(self):
        # Create a simple icon (Green square inside black)
        width = 64
        height = 64
        color_bg = "black"
        color_fg = "#00FF00" # Green
        image = Image.new('RGB', (width, height), color_bg)
        dc = ImageDraw.Draw(image)
        # Draw a 'mouse' shape or just a square
        dc.rectangle((16, 16, 48, 48), fill=color_fg)
        return image

    def show_window_from_tray(self, icon=None, item=None):
        self.root.after(0, self.restore_window)

    def restore_window(self):
        self.root.deiconify()
        self.visible = True
        # Bring to front
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        self.save_config() # Save on minimize/hide
        self.root.withdraw()
        self.visible = False

    def quit_app(self, icon=None, item=None):
        self.save_config() # Save on quit
        self.program_running = False
        if self.icon:
            self.icon.stop()
        self.root.quit()

    def find_minecraft_window(self):
        while self.program_running:
            found = False
            def callback(hwnd, windows):
                try:
                    title = win32gui.GetWindowText(hwnd)
                    if win32gui.IsWindowVisible(hwnd) and "Minecraft" in title:
                        windows.append((hwnd, title))
                except Exception:
                    pass
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if windows:
                self.target_hwnd = windows[0][0]
                self.window_status_var.set(f"Objetivo: {windows[0][1]}")
                self.window_label.configure(foreground="green")
            else:
                self.target_hwnd = None
                self.window_status_var.set("Minecraft no encontrado (Pausado)")
                self.window_label.configure(foreground="red")

            time.sleep(2)

    def toggle_clicking(self):
        if not self.target_hwnd and not self.running:
            self.status_var.set("Error: No window")
            return

        self.running = not self.running
        if self.running:
            self.status_var.set("ACTIVO (2do Plano)")
            self.status_label.configure(foreground="green")
            self.interval_entry.config(state='disabled')
            # Sound ON
            winsound.Beep(1000, 200) 
        else:
            self.status_var.set("Detenido")
            self.status_label.configure(foreground="red")
            self.interval_entry.config(state='normal')
            # Sound OFF
            winsound.Beep(500, 200)

    def on_press(self, key):
        try:
            if key == keyboard.Key.f6:
                self.root.after(0, self.toggle_clicking)
            elif key == keyboard.Key.f7:
                self.root.after(0, self.toggle_visibility)
        except AttributeError:
            pass

    def toggle_visibility(self):
        if self.visible:
            self.hide_window()
        else:
            self.restore_window()

    def clicker_loop(self):
        while self.program_running:
            if self.running and self.target_hwnd:
                try:
                    base_interval = float(self.interval_var.get())
                except ValueError:
                    base_interval = 1.0
                
                # Humanization logic
                sleep_time = base_interval
                if self.randomize_var.get():
                    variation = base_interval * 0.1 # 10% variation
                    sleep_time = base_interval + random.uniform(-variation, variation)
                    if sleep_time < 0.1: sleep_time = 0.1 # Minimum safety

                # Click logic
                click_type = self.click_type_var.get()
                if click_type == "Izquierdo":
                    down_msg = win32con.WM_LBUTTONDOWN
                    up_msg = win32con.WM_LBUTTONUP
                    btn_code = win32con.MK_LBUTTON
                else:
                    down_msg = win32con.WM_RBUTTONDOWN
                    up_msg = win32con.WM_RBUTTONUP
                    btn_code = win32con.MK_RBUTTON
                
                # Send background click
                win32api.PostMessage(self.target_hwnd, down_msg, btn_code, 0)
                time.sleep(0.05 + random.uniform(0, 0.05)) # Randomize press duration slightly
                win32api.PostMessage(self.target_hwnd, up_msg, 0, 0)
                
                time.sleep(sleep_time)
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
