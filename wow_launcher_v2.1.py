import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import sys

VERSION = "v2.1"
AUTHOR = "Gonza"
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

# ======================
# 🎨 UI
# ======================

root = tk.Tk()
root.title("WoW Realmlist Launcher - Created by GRaffaDev")
root.geometry("360x360")
root.resizable(False, False)
root.config(bg="#1c1c1c")

try:
    icon_path = os.path.join(sys._MEIPASS, "wow.ico") if getattr(sys, "frozen", False) else "wow.ico"
    root.iconbitmap(icon_path)
except:
    pass

titulo = tk.Label(
    root,
    text="WoW Realmlist Launcher V2.1",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1c1c1c"
)
titulo.pack(pady=15)
footer = tk.Label(
    root,
    text=f"WoW Realmlist Launcher {VERSION} — Developed by {AUTHOR}",
    font=("Segoe UI", 9),
    fg="#888",
    bg="#1c1c1c"
)
footer.pack(side="bottom", pady=8)

btn_config = tk.Button(
    root,
    text="📂 Configurar WoW",
    font=("Segoe UI", 11, "bold"),
    width=22,
    height=2,
    command=seleccionar_wow
)
btn_config.pack(pady=10)

for nombre in REALMS:
    btn = tk.Button(
        root,
        text=nombre,
        font=("Segoe UI", 11, "bold"),
        width=22,
        height=2,
        command=lambda n=nombre: cambiar_realm(n)
    )
    btn.pack(pady=5)

footer = tk.Label(
    root,
    text="Fan-made launcher — by Gonza",
    font=("Segoe UI", 9),
    fg="#888",
    bg="#1c1c1c"
)
footer.pack(side="bottom", pady=8)

root.mainloop()
