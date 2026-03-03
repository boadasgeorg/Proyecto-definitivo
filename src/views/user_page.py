""" ************************** 
    ***     USER PAGE      *** 
    ************************** """
# Este archivo contiene la clase UserPage que se encarga de gestionar la interfaz de usuario.

# --- Importaciones ---
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# --- Clase principal ---
class UserPage(ctk.CTkFrame):
    def __init__(self, master, on_logout, controller):
        super().__init__(master, fg_color="transparent")
        self.on_logout = on_logout
        self.controller = controller
        
        self.setup_ui()

    # --- Función de configuración de la interfaz ---
    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, height=70, corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        ctk.CTkLabel(self.header, text="Seith - Identificación", font=("Segoe UI", 20, "bold"), text_color="cyan").pack(side="left", padx=20, pady=15)
        ctk.CTkButton(self.header, text="Cerrar Sesión", width=100, corner_radius=15, fg_color="#CC0000", command=self.on_logout).pack(side="right", padx=20, pady=15)

        # Layout Centrado
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Contenedor Central: Resultados y Herramientas
        self.center_col = ctk.CTkScrollableFrame(self.main_container, width=600, corner_radius=20)
        self.center_col.pack(expand=True, fill="both", padx=100)
 
        ctk.CTkLabel(self.center_col, text="Panel de Categorización Taxonómica", font=("Segoe UI", 22, "bold"), text_color="cyan").pack(pady=20)
        
        # --- NUEVO: Selección de Rasgos Estructurados ---
        self.manual_frame = ctk.CTkFrame(self.center_col, corner_radius=15, fg_color="#1a1a1a")
        self.manual_frame.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(self.manual_frame, text="Seleccione los rasgos observados en el espécimen:", font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=15)
        
        # Selectores
        traits_grid = ctk.CTkFrame(self.manual_frame, fg_color="transparent")
        traits_grid.pack(pady=10)

        ctk.CTkLabel(traits_grid, text="Forma Caparazón:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.opt_shape = ctk.CTkOptionMenu(traits_grid, width=200, values=["no observado", "ovalado", "subcilindrico", "redondeado"], command=lambda x: self.refresh_identification())
        self.opt_shape.grid(row=0, column=1, pady=5, padx=10)

        ctk.CTkLabel(traits_grid, text="Superficie:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.opt_surf = ctk.CTkOptionMenu(traits_grid, width=200, values=["no observado", "liso", "rugoso", "estriado"], command=lambda x: self.refresh_identification())
        self.opt_surf.grid(row=1, column=1, pady=5, padx=10)

        ctk.CTkLabel(traits_grid, text="Dáctilo (Pata):", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.opt_dact = ctk.CTkOptionMenu(traits_grid, width=200, values=["no observado", "recto", "falcado"], command=lambda x: self.refresh_identification())
        self.opt_dact.grid(row=2, column=1, pady=5, padx=10)

        ctk.CTkLabel(traits_grid, text="Talla Estimada:", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.opt_size = ctk.CTkOptionMenu(traits_grid, width=200, values=["no observado", "pequeño", "mediano", "grande"], command=lambda x: self.refresh_identification())
        self.opt_size.grid(row=3, column=1, pady=5, padx=10)
 
        self.fb_label = ctk.CTkLabel(self.center_col, text="Complete los rasgos para iniciar la inferencia", text_color="cyan", font=("Segoe UI", 12, "italic"))
        self.fb_label.pack(pady=5)

        self.results_scroll = ctk.CTkFrame(self.center_col, corner_radius=15, fg_color="transparent")
        self.results_scroll.pack(fill="x", padx=40, pady=10)
 
        # --- Sección de Orientador IA ---
        self.ai_frame = ctk.CTkFrame(self.center_col, corner_radius=15, border_width=1, border_color="#004d4d")
        self.ai_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(self.ai_frame, text="🤖 Orientador Experto (IA)", font=("Segoe UI", 14, "bold"), text_color="cyan").pack(pady=10)
        
        self.api_key_entry = ctk.CTkEntry(self.ai_frame, placeholder_text="Pegue su Groq API Key aquí", height=30, font=("Segoe UI", 10), show="*")
        self.api_key_entry.pack(fill="x", padx=20, pady=5)
        
        user_key = getattr(self.controller, 'user_api_key', None)
        if user_key:
            self.api_key_entry.insert(0, user_key)
        
        self.ai_output = ctk.CTkTextbox(self.ai_frame, height=200, font=("Segoe UI", 11, "italic"), fg_color="#0a0a0a", corner_radius=10)
        self.ai_output.pack(fill="x", padx=20, pady=10)
        self.ai_output.insert("0.0", "🤖 Soy SEITH el Experto.\n\nCategoriza el espécimen usando los selectores superiores para que pueda darte un sustento científico.")
 
        self.ai_question_entry = ctk.CTkEntry(self.ai_frame, placeholder_text="Pregunta algo al experto...", height=35)
        self.ai_question_entry.pack(fill="x", padx=20, pady=5)
        self.ai_question_entry.bind("<Return>", lambda e: self.ask_question())
 
        self.btn_chat = ctk.CTkButton(
            self.ai_frame, text="CHATEAR CON EL EXPERTO", height=40, corner_radius=20, fg_color="#006666",
            command=self.ask_question
        )
        self.btn_chat.pack(pady=15)
 
        self.btn_export = ctk.CTkButton(
            self.center_col, text="", corner_radius=15, height=50,
            fg_color="#2B2B2B", state="", font=("Segoe UI", 14, "bold"), command=self.export_pdf
        )
        self.btn_export.pack(pady=20, padx=40)
 
        self.after(500, self.show_welcome_dialog)
 
    def show_welcome_dialog(self):
        """Muestra una ventana de guía rápida al iniciar."""
        welcome = ctk.CTkToplevel(self)
        welcome.title("Guía de Usuario - SEITH")
        welcome.geometry("550x600")
        welcome.resizable(False, False)
        welcome.grab_set() 
        
        x = self.master.winfo_x() + 275
        y = self.master.winfo_y() + 75
        welcome.geometry(f"+{x}+{y}")
 
        ctk.CTkLabel(welcome, text="👋 ¡Bienvenido a SEITH!", font=("Segoe UI", 24, "bold"), text_color="cyan").pack(pady=20)
        
        guide_text = (
            "Este sistema experto permite la identificación taxonómica de la familia Hippidae "
            "mediante un proceso de categorización manual asistida.\n\n"
            "INSTRUCCIONES DE USO:\n\n"
            "1. OBSERVACIÓN: Examine el espécimen y determine sus rasgos clave.\n"
            "2. CATEGORIZACIÓN: Seleccione los valores correspondientes en el panel central.\n"
            "3. INFERENCIA: El sistema calculará automáticamente las probabilidades.\n"
            "4. CONSULTA: Use al 'Orientador IA' para obtener detalles biológicos específicos.\n"
            "RECUERDA:\n"
            "El éxito de la identificación depende de la precisión de tus observaciones."
        )
        
        txt = ctk.CTkTextbox(welcome, height=250, font=("Segoe UI", 12), fg_color="transparent", border_width=0)
        txt.pack(fill="x", padx=30)
        txt.insert("0.0", guide_text)
        txt.configure(state="disabled")

        # Enlace a Groq
        link = ctk.CTkLabel(welcome, text="https://console.groq.com/keys", font=("Segoe UI", 12, "underline"), text_color="cyan", cursor="hand2")
        link.pack(pady=0)
        link.bind("<Button-1>", lambda e: os.startfile("https://console.groq.com/keys"))

        ctk.CTkLabel(welcome, text="(Haz clic arriba para ir a la web de Groq)", font=("Segoe UI", 10, "italic")).pack(pady=5)


        ctk.CTkButton(welcome, text="¡ENTENDIDO, EMPECEMOS!", height=45, corner_radius=22, command=welcome.destroy).pack(pady=40)

    def ask_question(self):
        """Maneja la conversación interactiva con el experto."""
        question = self.ai_question_entry.get().strip()
        if not question: return
        
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Falta API Key", "Introduce tu Groq API Key.")
            return

        self.controller.set_ai_api_key(api_key)
        self.controller.save_api_key(api_key) # Guardar permanentemente
        
        # Mostrar pregunta en el box
        self.ai_output.insert("end", f"\n\n👤 Estudiante: {question}")
        self.ai_output.see("end")
        self.ai_question_entry.delete(0, "end")
        
        def do_chat():
            results = getattr(self, 'current_full_results', None)
            answer = self.controller.chat_with_ai(question, results)
            self.ai_output.insert("end", f"\n\n🤖 Experto: {answer}")
            self.ai_output.see("end")

        import threading
        threading.Thread(target=do_chat).start()

    def consult_ai(self):
        """Envía el contexto actual a Gemini para obtener una explicación."""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Falta API Key", "Por favor, introduce tu Groq API Key para usar la IA.")
            return

        self.controller.set_ai_api_key(api_key)
        self.controller.save_api_key(api_key) # Guardar permanentemente
        self.ai_output.delete("0.0", "end")
        self.ai_output.insert("0.0", "Consultando al experto... 🧠")
        
        def run_ai_query():
            explanation = self.controller.get_ai_explanation(self.current_full_results)
            self.ai_output.delete("0.0", "end")
            self.ai_output.insert("0.0", explanation)

        # Ejecutamos en un thread pequeño para no congelar la UI si tarda
        import threading
        threading.Thread(target=run_ai_query).start()

    def refresh_identification(self):
        """Vuelve a ejecutar el motor experto sumando los rasgos seleccionados en los menús."""
        selected_traits = []
        
        # Recolectar solo lo que no sea "no observado"
        if self.opt_shape.get() != "no observado": selected_traits.append(self.opt_shape.get())
        if self.opt_surf.get() != "no observado": selected_traits.append(self.opt_surf.get())
        if self.opt_dact.get() != "no observado": selected_traits.append(self.opt_dact.get())
        if self.opt_size.get() != "no observado": selected_traits.append(self.opt_size.get())
        
        if not selected_traits:
            self.fb_label.configure(text="Seleccione al menos un rasgo", text_color="yellow")
            return

        # Llamar al motor experto a través del controlador
        res_list = self.controller.identify_by_manual_selection(selected_traits)
        self.current_full_results = res_list
        self.btn_export.configure(state="normal" if res_list else "disabled")
        
        self.display_results({"status": "success", "results": res_list})

    def export_pdf(self):
        if hasattr(self, 'current_full_results'):
            img_to_pdf = getattr(self, 'current_ref_path', None)
            ai_conv = self.ai_output.get("0.0", "end")
            
            pdf_path = self.controller.generate_id_report(img_to_pdf, self.current_full_results, ai_conv)
            messagebox.showinfo("Reporte Generado", f"PDF guardado en Descargas:\n{os.path.basename(pdf_path)}")
            os.startfile(os.path.dirname(pdf_path))

    # -- Función de selección de imagen (Solo Referencia) --
    def pick_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
        if path:
            self.current_ref_path = path
            my_image = ctk.CTkImage(light_image=Image.open(path), size=(360, 360))
            self.img_label.configure(image=my_image, text="")
            self.fb_label.configure(text="Imagen cargada como referencia", text_color="cyan")

    # -- Función de mostrar resultados --
    def display_results(self, data):
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        if data["status"] == "success":
            results = data.get("results", [])
            
            if not results:
                ctk.CTkLabel(self.results_scroll, text="No se encontraron coincidencias exactas.\nIntenta variar los rasgos observados.", font=("Segoe UI", 12, "italic"), text_color="gray").pack(pady=20)
                return

            # Actualizar label de estado
            self.fb_label.configure(text=f"Resultados Encontrados: {len(results)}", text_color="cyan")
            
            for r in results:
                card = ctk.CTkFrame(self.results_scroll, corner_radius=12, fg_color="#1a1a1a")
                card.pack(fill="x", pady=5, padx=5)
                
                content_frame = ctk.CTkFrame(card, fg_color="transparent")
                content_frame.pack(fill="x", padx=10, pady=10)

                # Info textual
                info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True)
                
                ctk.CTkLabel(info_frame, text=f"{r['genus']} {r['species']}", font=("Segoe UI", 14, "bold"), text_color="cyan").pack(anchor="w")
                ctk.CTkLabel(info_frame, text=f"Nombre común: {r['common_name']}", font=("Segoe UI", 11)).pack(anchor="w")
                ctk.CTkLabel(info_frame, text=f"Confianza diagnóstica: {r['probability']}%", font=("Segoe UI", 10)).pack(anchor="w")
                
                prog = ctk.CTkProgressBar(info_frame, width=150)
                prog.pack(pady=5, anchor="w")
                prog.set(r['probability']/100)

                # Imagen de referencia
                if r.get("ref_image"):
                    abs_path = os.path.join(os.getcwd(), r["ref_image"])
                    if os.path.exists(abs_path):
                        from PIL import Image
                        try:
                            ref_img_ctk = ctk.CTkImage(Image.open(abs_path), size=(70, 70))
                            ctk.CTkLabel(content_frame, image=ref_img_ctk, text="").pack(side="right")
                        except:
                            pass
        else:
            self.fb_label.configure(text=data["message"], text_color="red")
