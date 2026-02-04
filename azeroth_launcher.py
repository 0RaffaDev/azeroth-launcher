import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
from PIL import Image, ImageTk
import webbrowser


# ======================
# CONFIG
# ======================

VERSION = "v3.5"
AUTHOR = "GRaffaDev"
CONFIG_FILE = "config.json"

REALMS = {
    "🔥 Warmane": "set realmlist logon.warmane.com",
    "⚔️ UltimoWoW": "set realmlist logon.ultimowow.com",
    "🇦🇷 WowPatagonia": "set realmlist logon.wow-patagonia.win"
}

# ======================
# UTIL
# ======================

def center_window(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ======================
# HOVER
# ======================

def hover_on(e):
    e.widget.config(bg="#333333", cursor="hand2", font=("Segoe UI", 13, "bold"))
    

def hover_off(e, bg):
    e.widget.config(bg=bg, cursor="",font=("Segoe UI", 12, "bold"))
    

def hover_top_on(e):
    e.widget.config( 
        fg = "#f5e6c8",
        bg = "#2e2e2e",
        relief = "raised",
        cursor="hand2"
    )
    

def hover_top_off(e):
    
    e.widget.config(fg="white", bg="#1f1f1f", cursor="",  )

def hover_donate_on(e):
    e.widget.config(bg="#2f2f2f", cursor="hand2", font=("Segoe UI", 11, "bold"))
    

def hover_donate_off(e):
    e.widget.config(bg="#202020", cursor="", font=("Segoe UI", 10, "bold"))
    

# ======================
# CONFIG FILE
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
# REALMS CONFIG
# ======================

if "realms" not in config:
    config["realms"] = {
        "🔥 Warmane": "set realmlist logon.warmane.com",
        "⚔️ UltimoWoW": "set realmlist logon.ultimowow.com",
        "🇦🇷 WowPatagonia": "set realmlist logon.wow-patagonia.win"
    }
    save_config(config)

REALMS = config["realms"]


# ======================
# WOW
# ======================

def seleccionar_wow():
    path = filedialog.askopenfilename(
        title="Seleccioná Wow.exe",
        filetypes=[("Wow.exe", "Wow.exe")]
    )
    if not path:
        return

    base_dir = os.path.dirname(path)
    realmlist = os.path.join(base_dir, "Data", "esES", "realmlist.wtf")

    if not os.path.exists(realmlist):
        messagebox.showerror("Error", "No se encontró realmlist.wtf")
        return

    config["wow_path"] = path
    config["realmlist_path"] = realmlist
    save_config(config)
    messagebox.showinfo("OK", "WoW configurado correctamente")

def cambiar_realm(nombre):
    if "wow_path" not in config:
        messagebox.showwarning("Configurar", "Primero configurá WoW")
        return
    try:
        with open(config["realmlist_path"], "w") as f:
            f.write(REALMS[nombre])
        os.startfile(config["wow_path"])
    except Exception as e:
        messagebox.showerror("Error", str(e))
def agregar_server():
    win = tk.Toplevel(root)
    win.title("Agregar Server")
    win.resizable(False, False)
    center_window(win, 350, 220)

    tk.Label(win, text="Nombre del server").pack(pady=(15, 5))
    name_entry = tk.Entry(win, width=40)
    name_entry.pack()

    tk.Label(win, text="Realmlist").pack(pady=(15, 5))
    realm_entry = tk.Entry(win, width=40)
    realm_entry.pack()

    def guardar():
        nombre = name_entry.get().strip()
        realm = realm_entry.get().strip()

        if not nombre or not realm:
            messagebox.showerror("Error", "Completá todos los campos")
            return

        REALMS[nombre] = realm
        config["realms"] = REALMS
        save_config(config)

        win.destroy()
        render_sidebar()

def quitar_server():
    if not REALMS:
        messagebox.showinfo("Info", "No hay servers para quitar")
        return

    win = tk.Toplevel(root)
    win.title("Quitar Server")
    win.resizable(False, False)
    center_window(win, 300, 200)

    var = tk.StringVar(value=list(REALMS.keys())[0])

    tk.Label(win, text="Seleccioná un server").pack(pady=10)

    for name in REALMS:
        tk.Radiobutton(win, text=name, variable=var, value=name).pack(anchor="w", padx=30)

    def borrar():
        del REALMS[var.get()]
        config["realms"] = REALMS
        save_config(config)

        win.destroy()
        render_sidebar()

    tk.Button(win, text="Eliminar", fg="red", command=borrar).pack(pady=20)


    tk.Button(win, text="Guardar", command=guardar).pack(pady=20)


def open_donation():
    webbrowser.open(DONATION_URL)

DONATION_URL = "https://cafecito.app/graffadev"
# ======================
# UI
# ======================

root = tk.Tk()
root.title("Azeroth Launcher")

WINDOW_W = 1100
WINDOW_H = 700
center_window(root, WINDOW_W, WINDOW_H)
root.resizable(False, False)

# ======================
# LAYOUT
# ======================

topbar = tk.Frame(root, bg="#1f1f1f", height=55)
topbar.pack(fill="x")

body = tk.Frame(root, bg="#121212")
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg="#181818", width=250)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


content = tk.Frame(body, bg="#0e0e0e")
content.pack(side="right", fill="both", expand=True)

# ======================
# RENDER
# ======================

def clear_content():
    for w in content.winfo_children():
        w.destroy()

def render_inicio():
    clear_content()

    canvas = tk.Canvas(content, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.update()

    img = Image.open(r"C:\Users\Gonzalo\Desktop\script wow\fondo_wow.jpg")
    img = img.resize((1400, 700))
    photo = ImageTk.PhotoImage(img)

    bg = canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo

    def mover():
        canvas.move(bg, -0.3, 0)
        _, _, x2, _ = canvas.bbox(bg)
        if x2 <= canvas.winfo_width():
            canvas.move(bg, canvas.winfo_width(), 0)
        canvas.after(40, mover)

    mover()

# -------- NOVEDADES (CARDS) --------

# -------- NOVEDADES (CARDS) --------

def render_novedades():
    clear_content()

    # ======================
    # DATA
    # ======================

    noticia_principal = {
    "titulo": "🚀 Azeroth Launcher v3.3",
    "texto": (
        "Actualización enfocada en identidad visual y experiencia de usuario.\n\n"
        "✨ Novedades principales:\n"
        "• Nueva sección de Novedades\n"
        "• Cards visuales\n"
        "• Mejor jerarquía de información y lectura más clara\n\n"
        "Este update marca un antes y un después en el launcher, "
    ),
    "img": "assets/v33.png"
}


    noticias_anteriores = [
          {
            "titulo": "🛠 Próximamente – v4.0",
            "texto": (
                "La siguiente gran actualización del launcher.\n\n"
                "🔮 En desarrollo:\n"
                "• Agregar / quitar servidores desde la interfaz\n"
                "• Mejoras en la sección Perfil\n"
                "• Gestión visual de addons\n"
                "Esta versión marcará el salto funcional del launcher."
            ),
            "img": ""
        },
        {
            "titulo": "👤 v3.2 – Sección Perfil",
            "texto": (
                "Primera implementación de la sección Perfil.\n\n"
                "• Estructura visual del perfil de usuario\n"
                "• Preparado para estadísticas por servidor\n"
                "• Base para preferencias personales y configuraciones futuras\n\n"
                "Este update sienta las bases del sistema de usuarios del launcher."
        ),
        "img": "assets/v32.png"
        },
        {
            "titulo": "🎨 v3.1 – Rediseño de Interfaz",
            "texto": (
                "Rediseño completo de la interfaz principal.\n\n"
                "• Nueva Topbar con navegación clara\n"
                "• Sidebar más limpia y funcional\n"
                "• Hover effects modernos y consistentes\n\n"
                "El launcher adopta una estética más oscura, moderna y estilo Blizzard."
            ),
            "img": "assets/v31.png"
        },
        {
            "titulo": "🔥 v1.0 – Lanzamiento Inicial",
            "texto": (
                "Primera versión funcional del Azeroth Launcher.\n\n"
                "El comienzo del proyecto y la base de todo lo que vino después.\n"
                "•Cambio de Realmlist (Unica Funcion)"
            ),
            "img": ""
        },
      
]


    index = {"value": 0}

    # ======================
    # LAYOUT BASE
    # ======================

    container = tk.Frame(content, bg="#0e0e0e")
    container.pack(fill="both", expand=True, padx=40, pady=30)

    # ======================
    # CARD PRINCIPAL (3D)
    # ======================

    shadow = tk.Frame(container, bg="#000000")
    shadow.pack(fill="x", pady=(0, 30), padx=(6, 6))

    main_card = tk.Frame(
        shadow,
        bg="#1f1f1f",
        padx=40,
        pady=30,
        highlightbackground="#3a3a3a",
        highlightthickness=1
    )
    main_card.pack(fill="x", padx=(0, 6), pady=(0, 6))

    # Imagen principal
    try:
        img = Image.open(noticia_principal["img"]).resize((960, 240))
        photo = ImageTk.PhotoImage(img)
        img_lbl = tk.Label(main_card, image=photo, bg="#1f1f1f")
        img_lbl.image = photo
        img_lbl.pack(fill="x", pady=(0, 20))
    except:
        pass

    tk.Label(
        main_card,
        text=noticia_principal["titulo"],
        fg="white",
        bg="#1f1f1f",
        font=("Segoe UI", 24, "bold"),
        anchor="w"
    ).pack(anchor="w", pady=(0, 15))

    tk.Label(
        main_card,
        text=noticia_principal["texto"],
        fg="#d0d0d0",
        bg="#1f1f1f",
        font=("Segoe UI", 13),
        justify="left",
        wraplength=900
    ).pack(anchor="w")

    # ======================
    # CARRUSEL (CARD 3D)
    # ======================

    carousel = tk.Frame(container, bg="#0e0e0e")
    carousel.pack(fill="x")

    btn_prev = tk.Button(
        carousel, text="◀", font=("Segoe UI", 18, "bold"),
        bg="#0e0e0e", fg="white", bd=0
    )
    btn_prev.pack(side="left", padx=10)

    card_shadow = tk.Frame(carousel, bg="#000000")
    card_shadow.pack(side="left", expand=True, padx=6, pady=6)

    card = tk.Frame(
        card_shadow,
        bg="#1f1f1f",
        padx=30,
        pady=20,
        highlightbackground="#3a3a3a",
        highlightthickness=1,
        width=600
    )
    card.pack(padx=(0, 6), pady=(0, 6))

    btn_next = tk.Button(
        carousel, text="▶", font=("Segoe UI", 18, "bold"),
        bg="#0e0e0e", fg="white", bd=0
    )
    btn_next.pack(side="left", padx=10)

    img_label = tk.Label(card, bg="#1f1f1f")
    img_label.pack(fill="x", pady=(0, 15))

    titulo = tk.Label(
        card, fg="white", bg="#1f1f1f",
        font=("Segoe UI", 18, "bold")
    )
    titulo.pack(anchor="w", pady=(0, 10))

    texto = tk.Label(
        card, fg="#bbbbbb", bg="#1f1f1f",
        font=("Segoe UI", 12),
        justify="left", wraplength=520
    )
    texto.pack(anchor="w")

    def render_card():
        n = noticias_anteriores[index["value"]]
        titulo.config(text=n["titulo"])
        texto.config(text=n["texto"])

        try:
            img = Image.open(n["img"]).resize((520, 160))
            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo)
            img_label.image = photo
        except:
            img_label.config(image="")

    def prev():
        index["value"] = (index["value"] - 1) % len(noticias_anteriores)
        render_card()

    def next_():
        index["value"] = (index["value"] + 1) % len(noticias_anteriores)
        render_card()

    btn_prev.config(command=prev)
    btn_next.config(command=next_)
    render_card()

def render_perfil():
    clear_content()

    card = tk.Frame(content, bg="#1c1c1c", padx=50, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="PERFIL",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg="#1c1c1c"
    ).pack(pady=(0, 15))

    tk.Label(
        card,
        text=(
            "Usuario: GRaffaDev\n\n"
            "Esta sección estará disponible en una futura versión.\n\n"
            "• Perfil por usuario\n"
            "• Preferencias\n"
            "• Estadísticas por servidor"
        ),
        font=("Segoe UI", 12),
        fg="#cccccc",
        bg="#1c1c1c",
       
    ).pack()

def render_addons():
    clear_content()

    card = tk.Frame(content, bg="#1c1c1c", padx=40, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="ADDONS",
        fg="white",
        bg="#1c1c1c",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=(0, 15))

    tk.Label(
        card,
        text="Gestión de addons próximamente.",
        fg="#cccccc",
        bg="#1c1c1c",
        font=("Segoe UI", 12)
    ).pack()

def render_about():
    clear_content()

    frame = tk.Frame(content, bg="#0e0e0e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="Azeroth Launcher",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="#0e0e0e"
    ).pack(pady=(0, 10))

    tk.Label(
        frame,
        text=f"Versión {VERSION}\nDesarrollado por {AUTHOR}",
        fg="#aaaaaa",
        bg="#0e0e0e",
        font=("Segoe UI", 12),
        justify="center"
    ).pack()

def change_section(sec):
    if sec == "Inicio":
        render_inicio()
    elif sec == "Novedades":
        render_novedades()
    elif sec == "Perfil":
        render_perfil()
    elif sec == "Addons":
        render_addons()
    elif sec == "About":
        render_about()

# ======================
# TOPBAR
# ======================

for sec in ["Inicio", "Novedades", "Addons", "Perfil", "About"]:
    b = tk.Button(
        topbar,
        text=sec,
        bg="#1f1f1f",
        fg="white",
        bd=0,
        font=("Segoe UI", 12, "bold"),
        command=lambda s=sec: change_section(s),
        height=3,
        padx=15
    )
    b.bind("<Enter>", hover_top_on)
    b.bind("<Leave>", hover_top_off)
    b.pack(side="left", padx=25, pady=10)

# ======================
# SIDEBAR
# ======================

# ===== CONTENEDOR SCROLLEABLE PARA SERVERS =====

servers_container = tk.Frame(sidebar, bg="#181818")
servers_container.pack(fill="both", expand=True, padx=15)

servers_canvas = tk.Canvas(
    servers_container,
    bg="#181818",
    highlightthickness=0
)
servers_canvas.pack(side="left", fill="both", expand=True)

servers_scroll = tk.Scrollbar(
    servers_container,
    orient="vertical",
    command=servers_canvas.yview
)
servers_scroll.pack(side="right", fill="y")

servers_canvas.configure(yscrollcommand=servers_scroll.set)

servers_frame = tk.Frame(servers_canvas, bg="#181818")
servers_window = servers_canvas.create_window(
    (0, 0),
    window=servers_frame,
    anchor="nw"
)

def update_scrollregion(event):
    servers_canvas.configure(scrollregion=servers_canvas.bbox("all"))

servers_frame.bind("<Configure>", update_scrollregion)

def resize_servers_frame(event):
    servers_canvas.itemconfig(servers_window, width=event.width)

servers_canvas.bind("<Configure>", resize_servers_frame)

# ======================
# RENDER SIDEBAR (SOLO SERVERS)
# ======================

def render_sidebar():
    for w in servers_frame.winfo_children():
        w.destroy()

    btn_cfg = tk.Button(
    sidebar,
    text="⚙️ Configurar WoW",
    command=seleccionar_wow,
    bg="#252525",
    fg="white",
    bd=0,
    height=3,
    font=("Segoe UI", 11, "bold"),
    padx=15,
    )
    btn_cfg.bind("<Enter>", hover_top_on)
    btn_cfg.bind("<Leave>", hover_top_off)
    btn_cfg.pack(fill="x", padx=15, pady=(0, 20))

    tk.Label(
        sidebar,
        text="SERVERS",
        fg="#aaaaaa",
        bg="#181818",
        font=("Segoe UI", 11, "bold"),
        height=3
    ).pack(pady=(20, 15))


    for nombre in REALMS:
        b = tk.Button(
            servers_frame,
            text=nombre,
            command=lambda n=nombre: cambiar_realm(n),
            bg="#252525",
            fg="white",
            bd=0,
            height=3,
            font=("Segoe UI", 12, "bold"),
            anchor="w",
            padx=15
        )
        b.bind("<Enter>", hover_on)
        b.bind("<Leave>", lambda e, bg="#252525": hover_off(e, bg))
        b.pack(fill="x", padx=5, pady=6)

# ======================
# BOTONES FIJOS SIDEBAR
# ======================


tk.Button(
    sidebar,
    text="+ Agregar server",
    command=agregar_server,
    bg="#202020",
    fg="white",
    bd=0,
    height=2
).pack(fill="x", padx=15, pady=(10, 5))

tk.Button(
    sidebar,
    text="- Quitar server",
    command=quitar_server,
    bg="#202020",
    fg="white",
    bd=0,
    height=2
).pack(fill="x", padx=15, pady=(0, 15))

donate_btn = tk.Button(
    sidebar,
    text="☕ Apoyar el proyecto",
    command=open_donation,
    bg="#202020",
    fg="#dddddd",
    bd=0,
    height=2,
    font=("Segoe UI", 10, "bold")
)
donate_btn.bind("<Enter>", hover_donate_on)
donate_btn.bind("<Leave>", hover_donate_off)
donate_btn.pack(side="bottom", fill="x", padx=15, pady=20)

# ======================
# START
# ======================

render_sidebar()
render_inicio()
root.mainloop()
