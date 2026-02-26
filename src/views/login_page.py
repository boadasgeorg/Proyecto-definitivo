""" ************************** 
    ***     LOGIN PAGE     *** 
    ************************** """
# Este archivo contiene la clase LoginPage que se encarga de gestionar la interfaz de inicio de sesión.

# --- Importaciones ---
from typing import Self
import customtkinter as ctk
from tkinter import messagebox
from tkinter import messagebox
import os
# ... el resto de tus imports

# --- Clase principal ---
class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_admin, on_user, controller):
        super().__init__(master, fg_color="transparent")
        self.on_admin = on_admin
        self.on_user = on_user
        self.controller = controller
        
        self.setup_ui()

    # --- Función de configuración de la interfaz ---
    def setup_ui(self):
        # Frame central con bordes muy redondeados
        self.card = ctk.CTkFrame(self, corner_radius=25, width=400, height=550)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Logo / Icono
        self.icon_label = ctk.CTkLabel(self.card, text="🔒", font=("Segoe UI", 80))
        self.icon_label.pack(pady=(40, 10))

        self.title_label = ctk.CTkLabel(
            self.card, 
            text="SEITH", 
            font=("Segoe UI", 40, "bold"), 
            text_color="#00FFFF" # Cyan
        )
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.card, 
            text="Identificación de Especie", 
            font=("Segoe UI", 14)
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Campos de entrada con bordes redondeados
        self.username = ctk.CTkEntry(
            self.card, 
            placeholder_text="Usuario", 
            width=300, 
            height=45, 
            corner_radius=15,
            border_color="#1a1a1a"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self.card, 
            placeholder_text="Contraseña", 
            width=300, 
            height=45, 
            corner_radius=15, 
            show="*",
            border_color="#1a1a1a"
        )
        self.password.pack(pady=10)

        # Botón redondeado premium
        self.btn_login = ctk.CTkButton(
            self.card, 
            text="INICIAR SESIÓN", 
            width=300, 
            height=50, 
            corner_radius=25,
            font=("Segoe UI", 14, "bold"),
            fg_color="#008080", # Teal
            hover_color="#006666",
            command=self.login_click
        )
        self.btn_login.pack(pady=(40, 10))

        # Enlaces inferiores (Registro y Olvido)
        links_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        links_frame.pack(pady=5)

        btn_register = ctk.CTkButton(
            links_frame, text="Registrarse", font=("Segoe UI", 11, "underline"), 
            fg_color="transparent", width=80, hover_color="#2a2a2a",
            command=self.show_register
        )
        btn_register.pack(side="left", padx=5)

        btn_forgot = ctk.CTkButton(
            links_frame, text="¿Olvidaste tu clave?", font=("Segoe UI", 11, "underline"), 
            fg_color="transparent", width=120, hover_color="#2a2a2a",
            command=self.show_forgot_password
        )
        btn_forgot.pack(side="left", padx=5)


# --- SECCIÓN DEL PORTAFOLIOS ---

        # --- PORTAFOLIO 1 (Georg) ---
        self.link3 = ctk.CTkLabel(self, text="Portafolio de Georg", 
                            font=("Segoe UI", 12, "underline"), text_color="cyan", cursor="hand2")
        self.link3.pack(pady=(5, 0))
        self.link3.bind("<Button-1>", lambda e: os.startfile("https://boadasgeorg.github.io/portafolio"))

        # --- PORTAFOLIO 2 (Daniela) ---
        self.link1 = ctk.CTkLabel(self, 
                            text="Portafolio de Daniela", 
                            font=("Segoe UI", 12, "underline"), 
                            text_color="cyan", 
                            cursor="hand2")
        self.link1.pack(pady=(5, 0))
        self.link1.bind("<Button-1>", lambda e: os.startfile("https://danielasrd.github.io/Portafolio"))

        # --- PORTAFOLIO 3 (Vicky) ---
        self.link2 = ctk.CTkLabel(self, 
                            text="Portafolio de Vicky", 
                            font=("Segoe UI", 12, "underline"), 
                            text_color="cyan", 
                            cursor="hand2")
        self.link2.pack(pady=(5, 0)) # Menos espacio arriba para que estén juntos
        self.link2.bind("<Button-1>", lambda e: os.startfile("https://vickyudo2003.github.io/Portafolio"))

        # Texto aclaratorio opcional
        ctk.CTkLabel(self, 
text="(Haz clic arriba para ver nuestros portafolios)", 
font=("Segoe UI", 10, "italic")).pack(pady=(0, 10))

    def show_register(self):
        """Muestra un diálogo de registro para nuevos alumnos."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Registro de Alumno")
        dialog.geometry("400x480")
        dialog.grab_set()
        
        # Centrar relativo a la app
        x = self.master.winfo_x() + 350
        y = self.master.winfo_y() + 150
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text="Crear Nueva Cuenta", font=("Segoe UI", 20, "bold"), text_color="#00FFFF").pack(pady=20)
        
        reg_user = ctk.CTkEntry(dialog, placeholder_text="Nombre de Usuario", width=250, height=40, corner_radius=10)
        reg_user.pack(pady=10)
        
        reg_pass = ctk.CTkEntry(dialog, placeholder_text="Contraseña", width=250, height=40, corner_radius=10, show="*")
        reg_pass.pack(pady=10)
        
        reg_confirm = ctk.CTkEntry(dialog, placeholder_text="Confirmar Contraseña", width=250, height=40, corner_radius=10, show="*")
        reg_confirm.pack(pady=10)

        def do_register():
            u, p, c = reg_user.get(), reg_pass.get(), reg_confirm.get()
            if not u or not p:
                messagebox.showwarning("Incompleto", "Todos los campos son obligatorios.")
                return
            if p != c:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            
            if self.controller.register(u, p):
                messagebox.showinfo("Éxito", f"¡Bienvenido {u}! Ya puedes iniciar sesión.")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Ese nombre de usuario ya está en uso.")

        ctk.CTkButton(dialog, text="REGISTRARME", width=200, height=45, corner_radius=22, fg_color="#008080", command=do_register).pack(pady=30)

    def show_forgot_password(self):
        """Mensaje simple para recuperación de cuenta."""
        messagebox.showinfo("Recuperación", "Por favor, contacte al profesor o al administrador del sistema para restablecer su acceso.")

    # --- Función de inicio de sesión ---
    def login_click(self):
        user = self.username.get()
        pwd = self.password.get()
        
        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        role = self.controller.login(user, pwd)
        
        if role:
            if role == "admin":
                self.on_admin()
            else:
                self.on_user()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


