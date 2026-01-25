import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import sys

VERSION = "v2.2"
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

    realmlist_path = os.path.join(
        base_dir, "Data", "esES", "realmlist.wtf"
    )

    if not os.path.exists(realmlist_path):
        messagebox.showerror(
            "Error",
            "❌ No se encontró realmlist.wtf\n¿Es un WoW 3.3.5?"
        )
        return

    config["wow_path"] = wow_path
    config["realmlist_path"] = realmlist_path
    save_config(config)

    messagebox.showinfo(
        "Listo",
        "✅ WoW configurado correctamente"
    )

def cambiar_realm(nombre):
    if "wow_path" not in config or "realmlist_path" not in config:
        messagebox.showwarning(
            "Configurar primero",
            "⚠️ Primero seleccioná tu Wow.exe"
        )
        return

    try:
        with open(config["realmlist_path"], "w") as f:
            f.write(REALMS[nombre])

        os.startfile(config["wow_path"])

        messagebox.showinfo(
            "Éxito",
            f"🌍 Realm cambiado a {nombre}\n🚀 Abriendo WoW..."
        )
 
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
    e.widget["background"] = "#f7c5c5"

def on_leave(e):
    e.widget["background"] = "#f0f0f0"

def on_enter_config(e):
    e.widget["background"] = "#fac8c8"

def on_leave_config(e):
    e.widget["background"] = "#f5f5f5"


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
root.config(bg="#1c1c1c")

try:
    icon_path = os.path.join(sys._MEIPASS, "wow.ico") if getattr(sys, "frozen", False) else "wow.ico"
    root.iconbitmap(icon_path)
except:
    pass
# ======================
# 📦 CONTENEDORES
# ======================

header = tk.Frame(root, bg="#1c1c1c")
header.pack(fill="x", pady=(20, 10))

body = tk.Frame(root, bg="#1c1c1c")
actions = tk.Frame(body, bg="#1c1c1c")
actions.pack(pady=(0, 25))
body.pack(expand=True)

footer = tk.Frame(root, bg="#1c1c1c")
footer.pack(fill="x", pady=10)

titulo = tk.Label(
    header,
    text="Cambiar servidor de WoW",
    fg="white",
    bg="#1c1c1c",
    font=("Segoe UI", 16, "bold")
)
titulo.pack()

footer = tk.Label(
    footer,
    text=f"WoW Realmlist Launcher {VERSION} — Developed by {AUTHOR}",
    font=("Segoe UI", 9),
    fg="#888",
    bg="#1c1c1c"
)
footer.pack(side="bottom", pady=8)

btn_config = tk.Button(
    actions,
    text="⚙️ Configurar WoW",
    font=("Segoe UI", 11, "bold"),
    width=22,
    height=2,
    command=seleccionar_wow,
   

)
btn_config.bind("<Enter>", on_enter_config)
btn_config.bind("<Leave>", on_leave_config)


btn_config.pack(pady=(0, 15))


for nombre in REALMS:
    btn = tk.Button(
        body,
        text=nombre,
        font=("Segoe UI", 12, "bold"),
        width=22,
        height=2,
        command=lambda n=nombre: cambiar_realm(n)
        
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=8)



root.mainloop()
