import tkinter as tk
from tkinter import messagebox
import os
import sys

# ======================
# 🔧 CONFIGURACIÓN
# ======================

# 👉 Ruta al archivo realmlist.wtf
# Cambiala si tu cliente está en otra carpeta
REALMLIST_PATH = r"C:\World of Warcraft 3.3.5 esES - WoWArg\Data\esES\realmlist.wtf"
WOW_PATH = r"C:\World of Warcraft 3.3.5 esES - WoWArg\Wow.exe"

# 👉 Servidores disponibles
REALMS = {
    "Warmane": "set realmlist logon.warmane.com",
    "UltimoWoW": "set realmlist logon.ultimowow.com",
    "WowPatagonia": "set realmlist logon.wow-patagonia.win"
}

# ======================
# ⚙️ FUNCIONES
# ======================

def cambiar_realm(servidor):
    try:
        # Cambia el realmlist
        with open(REALMLIST_PATH, "w") as file:
            file.write(REALMS[servidor])

        # Abre WoW
        os.startfile(WOW_PATH)

        messagebox.showinfo(
            "Listo",
            f"✅ Realm cambiado a {servidor}\n🚀 Abriendo World of Warcraft..."
        )

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "❌ No se encontró el realmlist o el Wow.exe\nRevisá las rutas."
        )

    except PermissionError:
        messagebox.showerror(
            "Error",
            "⚠️ Ejecutá el launcher como administrador."
        )
# ======================
# 🎨 INTERFAZ
# ======================

root = tk.Tk()
root.title("WoW Realmlist Switcher")

try:
    icon_path = os.path.join(sys._MEIPASS, "wow.ico") if getattr(sys, 'frozen', False) else "wow.ico"
    root.iconbitmap(icon_path)
except:
    pass

root.config(bg="#1c1c1c")
root.update_idletasks()
root.resizable(False, False)

titulo = tk.Label(root, text="Cambiar servidor de WoW", fg="white", bg="#1c1c1c", font=("Segoe UI", 14, "bold"))
titulo.pack(pady=20)

for nombre, realm in REALMS.items():
    btn = tk.Button(root, text=nombre, font=("Segoe UI", 12, "bold"),
                    width=20, height=2,
                    command=lambda n=nombre: cambiar_realm(n))
    btn.pack(pady=6)


footer = tk.Label(root, text="by Gonza — v1.0", fg="#888", bg="#1c1c1c", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=5)

root.mainloop()
