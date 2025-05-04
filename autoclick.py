import pyautogui
import keyboard
import time
import threading
import random
import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

class RapidClickVisualizer:
    def __init__(self):
        self.running = False
        self.zone = None
        self.click_thread = None
        self.click_count = 0
        self.click_speed = 10  # clicks por segundo
        self.dot_size = 5  # tamaño del punto visual
        self.dot_duration = 0.2  # segundos que se muestra el punto
        self.last_dot_time = 0
        self.dot_window = None
        self.setup_ui()
        self.setup_hotkeys()
        
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Control de RapidClick")
        self.root.geometry("300x200")
        
        tk.Label(self.root, text="Velocidad (clicks/seg):").pack()
        self.speed_slider = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL)
        self.speed_slider.set(self.click_speed)
        self.speed_slider.pack()
        
        tk.Label(self.root, text="Tamaño del punto:").pack()
        self.size_slider = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL)
        self.size_slider.set(self.dot_size)
        self.size_slider.pack()
        
        tk.Label(self.root, text="Duración del punto (s):").pack()
        self.duration_slider = tk.Scale(self.root, from_=0.1, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.duration_slider.set(self.dot_duration)
        self.duration_slider.pack()
        
        tk.Button(self.root, text="Salir", command=self.clean_exit).pack(pady=10)
        
        # Actualizar parámetros en tiempo real
        self.speed_slider.bind("<Motion>", lambda e: self.update_params())
        self.size_slider.bind("<Motion>", lambda e: self.update_params())
        self.duration_slider.bind("<Motion>", lambda e: self.update_params())
        
    def update_params(self):
        self.click_speed = self.speed_slider.get()
        self.dot_size = self.size_slider.get()
        self.dot_duration = self.duration_slider.get()
        
    def setup_hotkeys(self):
        print("Sistema de RapidClick iniciado. Instrucciones:")
        print("1. Presiona Ctrl+H para iniciar/seleccionar zona")
        print("2. Presiona Ctrl+J para detener")
        
        keyboard.add_hotkey('ctrl+h', self.start_autoclick)
        keyboard.add_hotkey('ctrl+j', self.stop_autoclick)
        
    def select_zone(self):
        print("Selecciona la zona de clicks:")
        print("1. Mueve el ratón a la esquina superior izquierda y presiona 's'")
        keyboard.wait('s')
        x1, y1 = pyautogui.position()
        
        print("2. Mueve el ratón a la esquina inferior derecha y presiona 's'")
        keyboard.wait('s')
        x2, y2 = pyautogui.position()
        
        self.zone = {
            'x1': min(x1, x2),
            'y1': min(y1, y2),
            'x2': max(x1, x2),
            'y2': max(y1, y2),
            'width': abs(x2 - x1),
            'height': abs(y2 - y1)
        }
        
        print(f"Zona seleccionada: {self.zone}")
        return True
        
    def show_click_dot(self, x, y):
        # Crea una ventana temporal para mostrar el punto
        if self.dot_window:
            try:
                self.dot_window.destroy()
            except:
                pass
        
        self.dot_window = tk.Toplevel(self.root)
        self.dot_window.overrideredirect(True)
        self.dot_window.geometry(f"+{x-self.dot_size}+{y-self.dot_size}")
        self.dot_window.attributes('-topmost', True)
        self.dot_window.attributes('-transparentcolor', 'white')
        
        canvas = tk.Canvas(self.dot_window, width=self.dot_size*2, height=self.dot_size*2, bg='white', highlightthickness=0)
        canvas.pack()
        canvas.create_oval(0, 0, self.dot_size*2, self.dot_size*2, fill='red', outline='red')
        
        self.last_dot_time = time.time()
        self.dot_window.after(int(self.dot_duration * 1000), self.dot_window.destroy)
        
    def rapid_click(self):
        while self.running:
            try:
                # Coordenadas aleatorias dentro de la zona
                x = random.randint(self.zone['x1'], self.zone['x2'])
                y = random.randint(self.zone['y1'], self.zone['y2'])
                
                # Movimiento rápido pero con pequeña variación humana
                pyautogui.moveTo(
                    x + random.randint(-2, 2), 
                    y + random.randint(-2, 2), 
                    duration=random.uniform(0.01, 0.05)
                
                # Click rápido
                pyautogui.click()
                self.click_count += 1
                
                # Mostrar punto visual
                self.root.after(0, lambda: self.show_click_dot(x, y))
                
                # Espera ajustable para velocidad
                time.sleep(1/self.click_speed)
                
            except Exception as e:
                print(f"Error: {e}")
                self.stop_autoclick()
                
    def start_autoclick(self):
        if not self.running:
            if self.zone is None:
                if not self.select_zone():
                    return
                    
            self.running = True
            self.click_thread = threading.Thread(target=self.rapid_click, daemon=True)
            self.click_thread.start()
            print(f"RapidClick iniciado a {self.click_speed} clicks/segundo")
        else:
            print("El RapidClick ya está en ejecución")
            
    def stop_autoclick(self):
        if self.running:
            self.running = False
            if self.click_thread is not None:
                self.click_thread.join(timeout=0.1)
            print(f"RapidClick detenido. Total clicks: {self.click_count}")
        else:
            print("El RapidClick no está en ejecución")
            
    def clean_exit(self):
        self.stop_autoclick()
        self.root.destroy()
        print("Programa terminado")
        exit()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    clicker = RapidClickVisualizer()
    try:
        clicker.run()
    except KeyboardInterrupt:
        clicker.clean_exit()