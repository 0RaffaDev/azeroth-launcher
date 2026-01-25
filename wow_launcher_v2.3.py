import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import sys
from PIL import Image, ImageTk

VERSION = "v2.3"
AUTHOR = "GRaffaDev"
CONFIG_FILE = "config.json"

REALMS = {
    "🔥 Warmane": "set realmlist logon.warmane.com",
    "⚔️ UltimoWoW": "set realmlist logon.ultimowow.com",
    "🌎 WowPatagonia": "set realmlist logon.wow-patagonia.win"
}

# ======================
# ⚙️ CONFIG
# ======================

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_config()

# ======================
# 🔧 FUNCIONES
# ======================

def seleccionar_wow():
    path = filedialog.askopenfilename(
        title="Seleccioná Wow.exe",
        filetypes=[("Wow.exe", "Wow.exe")]
    )
    if not path:
        return

    wow_path = path
    base_dir = os.path.dirname(wow_path)
    realmlist_path = os.path.join(base_dir, "Data", "esES", "realmlist.wtf")

    if not os.path.exists(realmlist_path):
        messagebox.showerror(
            "Error",
            "❌ No se encontró realmlist.wtf\n¿Es un WoW 3.3.5?"
        )
        return

    config["wow_path"] = wow_path
    config["realmlist_path"] = realmlist_path
    save_config(config)
    messagebox.showinfo("Listo", "✅ WoW configurado correctamente")

def cambiar_realm(nombre):
    if "wow_path" not in config or "realmlist_path" not in config:
        messagebox.showwarning(
            "Configurar primero",
            "⚠️ Primero seleccioná tu Wow.exe"
        )
        return
    try:
        for child in botones_frame.winfo_children():
            child.config(state="disabled")
        with open(config["realmlist_path"], "w") as f:
            f.write(REALMS[nombre])
        os.startfile(config["wow_path"])
        messagebox.showinfo(
            "Éxito",
            f"🌍 Realm cambiado a {nombre}\n🚀 Abriendo WoW..."
        )
        for child in botones_frame.winfo_children():
            child.config(state="normal")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def center_window(root, width, height):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
def on_enter(e):
    e.widget["background"] = "#444444"  # resalta un poco
    e.widget["fg"] = "white"
    e.widget.config(cursor="hand2")

def on_leave(e):
    e.widget["background"] = "#1c1c1c"  # vuelve al fondo oscuro
    e.widget["fg"] = "white"
    e.widget.config(cursor="")

def on_enter_config(e):
    e.widget["background"] = "#fac8c8"
    e.widget["fg"] = "#1c1c1c"
    e.widget.config(cursor="hand2")

def on_leave_config(e):
    e.widget["background"] = "#f5f5f5"
    e.widget["fg"] = "black"
    e.widget.config(cursor="")

# ======================
# 🎨 UI
# ======================

root = tk.Tk()
root.title("WoW Realmlist Launcher - Created by GRaffaDev")
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)
root.resizable(False, False)

try:
    icon_path = os.path.join(sys._MEIPASS, "wow.ico") if getattr(sys, "frozen", False) else "wow.ico"
    root.iconbitmap(icon_path)
except:
    pass

# ======================
# 🌌 Canvas de fondo animado (imagen JPG)
# ======================
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Carga la imagen
bg_image = Image.open(r"C:\Users\Gonzalo\Desktop\script wow\fondo_wow.jpg").resize((WINDOW_WIDTH*2, WINDOW_HEIGHT))  # doble ancho para scroll
bg_photo = ImageTk.PhotoImage(bg_image)
bg_item = canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Animación simple: movimiento horizontal
def mover_fondo():
    canvas.move(bg_item, -1, 0)  # mueve 1px a la izquierda
    x1, y1, x2, y2 = canvas.bbox(bg_item)
    if x2 <= WINDOW_WIDTH:
        canvas.move(bg_item, WINDOW_WIDTH, 0)  # loop infinito
    canvas.after(50, mover_fondo)

mover_fondo()

# ======================
# 📦 Contenedores y botones sobre canvas
# ======================

# Header
header = tk.Frame(canvas, bg="#000000", bd=0)
canvas.create_window(WINDOW_WIDTH//2, 40, window=header)
titulo = tk.Label(
    header,
    text="Cambiar servidor de WoW",
    fg="white",
    bg=None,
    font=("Segoe UI", 16, "bold")
)
titulo.pack()

# Botones
botones_frame = tk.Frame(canvas, bg="", bd=0)
canvas.create_window(WINDOW_WIDTH//2, 250, window=botones_frame)

btn_config = tk.Button(
    botones_frame,
    text="⚙️ Configurar WoW",
    font=("Segoe UI", 11, "bold"),
    width=22,
    height=2,
    command=seleccionar_wow,
    bg=None,   # mismo color del header/fondo oscuro
    fg="white",
    bd=0,
    highlightthickness=0,
    activebackground="#333333",  # cuando hover/click
    activeforeground="white"
)


btn_config.bind("<Enter>", on_enter_config)
btn_config.bind("<Leave>", on_leave_config)
btn_config.pack(pady=(0,15))

for nombre in REALMS:
    btn = tk.Button(
        botones_frame,
        text=nombre,
        font=("Segoe UI", 12, "bold"),
        width=22,
        height=2,
        command=lambda n=nombre: cambiar_realm(n),
        bg=None
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=8)

# Footer
footer = tk.Label(
    canvas,
    text=f"WoW Realmlist Launcher {VERSION} — Developed by {AUTHOR}",
    font=("Segoe UI", 9),
    fg="#ccc",
    bg="#000000"
)
canvas.create_window(WINDOW_WIDTH//2, WINDOW_HEIGHT-20, window=footer)

root.mainloop()
