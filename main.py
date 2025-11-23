import os
import threading
import time
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import webbrowser
from system_actions import SystemActions, SERVICE_INFO
from log_panel import LogPanel
from typing import Callable


class Window:

    def __init__(self, width: int = 1200, height: int = 850) -> None:
        """
        Initializes the main window of the System Optimizer.

        :param: width (int): Window width in pixels. Default: 600
        :param: height (int): Window height in pixels. Default: 650
        """

        self.root = tk.Tk()
        self.root.configure(bg="#e6e9ef")
        self.root.title("System Optimizer")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, True)

        self.center_window(width, height)

        # Create the in the top of the window
        self.create_title()

        # Add a separator
        separator = tk.Frame(self.root, height=2, bg="#0056b3")
        separator.pack(fill=tk.X)

        # Shadow Effect Container (Card)
        shadow_frame = tk.Frame(self.root, bg="#d0d4da")
        shadow_frame.pack(pady=(30, 0), padx=(50, 50), fill=tk.BOTH, expand=True)

        inner_shadow = tk.Frame(shadow_frame, bg="#e2e6eb")
        inner_shadow.pack(pady=3,  padx=3, fill=tk.BOTH, expand=True)

        # Central container (card)
        self.container = tk.Frame(inner_shadow, bg="#ffffff", bd=0, relief=tk.FLAT)
        self.container.pack(pady=0, padx=0, fill=tk.BOTH, expand=True)

        # Side panel logs
        self.log_panel = LogPanel(self.container)
        self.log_panel.frame.grid(row=0, column=1, sticky="ns")

        # System actions using the logs panel
        self.actions = SystemActions(self.log_panel)

        # Create layout in columns within card
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # Frame buttons
        self.button_frame = tk.Frame(self.container, bg="#ffffff")
        self.button_frame.grid(row=0, column=0, sticky="nsew", padx=(30, 10), pady=20)

        # Create the main menu buttons.
        self.create_buttons()

        # Create footer
        self.create_footer()

        # print(self.root.winfo_rootx(), self.root.winfo_rooty(), self.root.winfo_width(), self.root.winfo_height())
        # Start the main loop.
        self.root.mainloop()


    def center_window(self, width: int, height: int) -> None:
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_title(self):
        """
        Creates the Optimizer title at the top of the window.

        :return: None
        """

        title_label = tk.Label(
            self.root,
            text="System Optimizer",
            font=("Arial", 16, "bold"),
            bg="#007bff",
            fg="white",
            padx=10,
            pady=10
        )
        title_label.pack(fill=tk.X, pady=(10, 5))

    # List of buttons: (Button text, function called)
    def create_buttons(self) -> None:
        """
        It creates the main menu buttons and arranges them vertically.

        :return: None
        """

        buttons = [

            ("PC Performance Test",
             lambda: self.run_with_overlay(
                 "Running Performance Test",
                 "Benchmarking CPU, RAM, Disk and GPU...",
                 self.actions.pc_performance_test
             ),
             "#ff6b6b"),

            ("Create Restore Point",
             lambda: self.run_with_overlay(
                 "Creating Restore Point",
                 "Windows is creating a safe system snapshot...",
                 self.actions.create_restore_point
             ),
             "#34495e"),

            ("Enable / Disable SysMain",
             lambda: self.toggle_service_with_overlay(
                 "SysMain",
                 "SysMain / SuperFetch",
                 "Manages performance optimization and app preloading."
             ),
             "#f5a623"),

            ("Clean Temporary Files",
             lambda: self.run_with_overlay(
                 "Cleaning Temporary Files",
                 "Removing temporary files…",
                 self.actions.clean_temporary_files
             ),
             "#32cd32"),

            ("Deep Cleaning",
             lambda: self.run_with_overlay(
                 "Deep System Cleanup",
                 "Cleaning WinSxS, Delivery Optimization, Logs, Updates…",
                 self.actions.deep_system_cleanup
             ),
             "#4b0082"),

            ("Enable High Performance Power Plan",
             lambda: self.run_with_overlay(
                 "Enabling High Performance Mode",
                 "Applying best-performance power settings…",
                 self.actions.enable_high_power_plan
             ),
             "#007bff"),

            ("Disable Background Apps",
             lambda: self.run_with_overlay(
                 "Disabling Background Apps",
                 "Blocking unnecessary app background activity…",
                 self.actions.disable_background_apps
             ),
             "#8e44ad"),

            ("Complete Optimization",
             lambda: self.run_with_overlay(
                 "Running Complete Optimization",
                 "Applying full system performance improvements…",
                 self.actions.complete_optimization
             ),
             "#2c3e50"),

            ("Update All Software",
             lambda: self.run_with_overlay(
                 "Updating Software",
                 "Checking and updating all installed applications…",
                 self.actions.update_software
             ),
             "#009688"),

            # Windows Services
            ("Windows Update Service",
             lambda: self.toggle_service_with_overlay(
                 "wuauserv",
                 "Windows Update Service",
                 "Handles system update download and installation."
             ),
             "#2980b9"),

            ("BITS Service",
             lambda: self.toggle_service_with_overlay(
                 "bits",
                 "Background Intelligent Transfer Service",
                 "Transfers files in background for Windows Update and apps."
             ),
             "#9b59b6"),

            ("Print Spooler",
             lambda: self.toggle_service_with_overlay(
                 "spooler",
                 "Print Spooler",
                 "Manages print queue and printer communication."
             ),
             "#e67e22"),

            ("Windows Search",
             lambda: self.toggle_service_with_overlay(
                 "WSearch",
                 "Windows Search Indexing",
                 "Indexes files to speed up search results."
             ),
             "#0099dd"),

            ("Telemetry (DiagTrack)",
             lambda: self.toggle_service_with_overlay(
                 "DiagTrack",
                 "Windows Telemetry",
                 "Collects diagnostics data for service improvement."
             ),
             "#aa44dd"),
        ]

        # Creation loop
        for text, command, color in buttons:
            btn = tk.Button(
                self.button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                activebackground=self.darken_color(color, 0.7),
                activeforeground="white",
                cursor="hand2"
            )
            btn.original_bg = color
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)
            btn.pack(pady=8, fill=tk.X)

    def create_footer(self) -> None:
        """
        Creates a footer with a clickable GitHub logo + link.

        :return: None
        """

        footer_frame = tk.Frame(self.root, bg="#0056b3")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Fixed text on the left
        label_left = tk.Label(
            footer_frame,
            text="© 2025 System Optimizer | Developed by Celmar",
            font=("Segoe UI", 9),
            bg="#0056b3",
            fg="white",
            pady=6
        )
        label_left.pack(side=tk.LEFT, padx=10, pady=6)

        # Link frame (logo + text side by side)
        link_frame = tk.Frame(footer_frame, bg="#0056b3")
        link_frame.pack(side=tk.RIGHT, padx=10)

        # Create a canvas for the circular logo
        canvas_size = 24
        canvas = tk.Canvas(
            link_frame,
            width=canvas_size,
            height=canvas_size,
            bg="#0056b3",
            highlightthickness=0
        )
        canvas.pack(side=tk.LEFT)

        # Draw the background circle
        radius = canvas_size // 2
        canvas.create_oval(0, 0, canvas_size, canvas_size, fill="#0056b3", outline="")

        # Load the resized image and add it to the canvas
        img_path = "./images/github_logo.png"
        img = self.create_rounded_image(img_path, size=(canvas_size, canvas_size), radius=radius)
        canvas.create_image(radius, radius, image=img)
        canvas.image = img
        canvas.config(cursor="hand2")

        # Link on the right
        github_link = tk.Label(
            link_frame,
            text="GitHub",
            font=("Segoe UI", 9, "underline"),
            bg="#0056b3",
            fg="#add8e6",
            cursor="hand2"
        )
        github_link.pack(side=tk.LEFT, padx=(4, 0))

        # Click event - opens the browser
        canvas.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/CelmarPA"))
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/CelmarPA"))

    def create_rounded_image(self, path: str, size: tuple[int, int], radius: int) -> ImageTk.PhotoImage:
        """
        Loads an image, resizes it, applies rounded corners, and returns a Tkinter-compatible PhotoImage.

        :param path: (str): Path to the image file.
        :param size: (tuple[int, int]): Desired size (width, height).
        :param radius: (int): Corner radius.
        :return ImageTk.PhotoImage: The ImageTk.PhotoImage (ready to use in Tkinter)
        """

        img = Image.open(path).resize(size, Image.Resampling.LANCZOS).convert("RGBA")

        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, *img.size), radius=radius, fill=255)

        img.putalpha(mask)

        return ImageTk.PhotoImage(img)

    def on_enter(self, event: tk.Event) -> None:
        color = event.widget.original_bg
        event.widget.config(background=self.darken_color(color), font=("Segoe UI", 11, "bold"))

    def on_leave(self, event: tk.Event) -> None:
        event.widget.config(background=event.widget.original_bg, font=("Segoe UI", 10, "bold"))

    def darken_color(self, hex_color: str, factor: float = 0.8) -> str:
        """
        Darkens a hex color by a given factor.
        Example:
            "#1e90ff" → "#1872cc" (if factor=0.8)

        param: hex_color (str): Color in hex format (e.g., "#1e90ff")
        param: factor (float): Darkening multiplier (0.0–1.0)

        :return str: The darkened color in hex format.
        """

        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * factor) for c in rgb)

        return "#%02x%02x%02x" % darker_rgb

    def run_feature_with_info(self, action: Callable[[], None], title: str, description: str, category: str, risk: str) -> None:
        proceed = show_feature_info(
            self.root,
            title=title,
            description=description,
            category=category,
            risk=risk,
        )

        if not proceed:
            if self.log_panel:
                self.log_panel.info("User cancelled operation.")

            return

        action()

    def run_with_overlay(self, title: str, message: str, task: Callable[[], None]) -> None:

        overlay = ProgressOverlay(self.root, title=title, message=message, slide=False)

        def worker():
            try:
                if hasattr(self, "log_panel"):
                    self.log_panel.info(f"▶️ {title}")

                task()

                overlay.update_status("Done")
                time.sleep(0.6)
                overlay.close()

                if hasattr(self, "log_panel"):
                    self.log_panel.success(f"{title} completed successfully.")
            except Exception as e:
                overlay.update_status("Error")
                time.sleep(0.6)
                overlay.close()

                if hasattr(self, "log_panel"):
                    self.log_panel.error(f"{title} failed: {e}")

                messagebox.showerror("Error", f"Operation failed:\n{e}")

        threading.Thread(target=worker, daemon=True).start()


    # Integration helper in main window class
    # Inside your Window class (or wherever you create buttons), add a method like this:
    def toggle_service_with_overlay(self, service_name: str, friendly_name: str, description: str) -> None:
        """
        Full flow:
        1) show feature info modal
        2) if user continues -> check state
        3) show overlay + spinner
        4) ask backend to toggle (async)
        5) finish callbacks update logs and UI
        """
        proceed = show_feature_info(
            self.root,
            title=f"{friendly_name}",
            description=description,
            category="Windows Service",
            risk="Low"
        )

        if not proceed:
            if self.log_panel:
                self.log_panel.info("User cancelled service operation.")
            return

        # Check current state
        status = self.actions._check_service_status(service_name)

        if status == "running":
            action = "disable"
            verb = "Disabling"
        else:
            action = "enable"
            verb = "Enabling"

        overlay = ProgressOverlay(self.root, title=f"{verb} {friendly_name}...",
                                  message=f"{verb} {friendly_name}. Please wait.")
        if self.log_panel:
            self.log_panel.info(f"▶️ {verb} {friendly_name}...")

        def on_start():
            try:
                overlay.update_status(f"{verb} ...")
            except Exception:
                pass

        def on_finish(success, stderr):
            try:
                if success:
                    overlay.update_status("Done!")
                    # let animation settle and close non-blocking
                    self.root.after(600, overlay.close)
                    if self.log_panel:
                        self.log_panel.success(f"{friendly_name} {action}d successfully.")
                    try:
                        messagebox.showinfo("Success", f"{friendly_name} updated successfully.")
                    except Exception:
                        pass
                else:
                    overlay.update_status("Failed")
                    self.root.after(600, overlay.close)
                    if self.log_panel:
                        self.log_panel.error(f"{friendly_name} toggle failed: {stderr}")
                    try:
                        messagebox.showerror("Error", f"Operation failed:\n{stderr}")
                    except Exception:
                        pass
            except Exception as e:
                try:
                    overlay.close()
                except Exception:
                    pass
                if self.log_panel:
                    self.log_panel.error(f"Finish callback exception: {e}")

        def on_error(exc):
            try:
                overlay.update_status("Error")
                self.root.after(400, overlay.close)
            except Exception:
                pass
            if self.log_panel:
                self.log_panel.error(f"Exception: {exc}")
            try:
                messagebox.showerror("Error", f"Exception: {exc}")
            except Exception:
                pass

        # start async toggle
        self.actions.toggle_service_async(
            service_name=service_name,
            action=action,
            on_start=on_start,
            on_finish=on_finish,
            on_error=on_error
        )

    def toggle_any_service(self, service_name: str) -> None:
        info = SERVICE_INFO.get(service_name)

        if not info:
            self.log_panel.error(f"Service not registered: {service_name}")
            return

        friendly = info["friendly"]
        description = info["description"]

        self.toggle_service_with_overlay(
            service_name,
            friendly,
            description
        )


class ProgressOverlay:
    def __init__(self, parent, title="Working...", message="", **_):
        self.parent = parent

        self.win = tk.Toplevel(parent)
        self.win.transient(parent)
        self.win.overrideredirect(True)

        self.win.update_idletasks()
        parent.update_idletasks()

        # pega posição absoluta com bordas e título
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()

        # pega tamanho TOTAL EXIBIDO
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        # AQUI ESTÁ A CORREÇÃO IMPORTANTE:
        # garantir que a janela já está 100% renderizada
        self.win.after(10, lambda: self.win.geometry(f"{pw}x{ph}+{px}+{py}"))

        print(px, py, pw, ph)

        # --- FUMAÇA (overlay escuro semi-transparente) ---
        self.win.configure(bg="black")
        self.win.attributes("-alpha", 0.45)  # Transparência real do overlay

        self.bg = tk.Frame(self.win, bg="black")
        self.bg.place(relwidth=1, relheight=1)

        # --- CARD CENTRAL ---
        card_w, card_h = 420, 160
        cx = (pw - card_w) // 2
        cy = (ph - card_h) // 2

        self.card = tk.Frame(self.win, bg="#e9eaed", bd=2, relief="raised")

        self.card.place(x=cx, y=cy, width=card_w, height=card_h)

        tk.Label(self.card, text=title, font=("Segoe UI", 12, "bold"), bg="white").pack(pady=(12,6))


        # --- SPINNER ---
        self.spinner = Spinner(self.card, folder="images/spinner", size=64)
        self.spinner.pack(pady=(6,4))

        self.status_lbl = tk.Label(self.card, text="Starting...", bg="white")
        self.status_lbl.pack()

        # Camadas corretas
        self.bg.lower()
        self.card.lift()
        self.spinner.lift()
        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.after(20, lambda: self.win.attributes("-topmost", False))

        # Garantir centralização mesmo após update
        self.win.after(10, self.center_card)

    def center_card(self):
        self.parent.update_idletasks()

        pw = self.parent.winfo_width()
        ph = self.parent.winfo_height()

        card_w = 420
        card_h = 160

        cx = (pw - card_w) // 2
        cy = (ph - card_h) // 2

        self.card.place(x=cx, y=cy, width=card_w, height=card_h)


    def update_status(self, text: str):
        self.status_lbl.config(text=text)
        self.win.update_idletasks()

    def close(self):
        """Fecha o overlay com segurança."""
        try:
            if self.win and self.win.winfo_exists():
                self.win.destroy()
        except Exception as e:
            print(f"Erro ao fechar overlay: {e}")


# Service explanation dialog
def show_feature_info(parent: tk.Tk, title: str, description: str, risk: str = "Low", category: str = "General") -> bool:
    """
    Universal info window for any feature, service or optimization action.
    Returns True if user clicks Continue.
    """
    modal = tk.Toplevel(parent)
    modal.transient(parent)
    modal.grab_set()
    modal.title(title)
    modal.geometry("520x330")
    modal.resizable(False, False)

    lbl_title = tk.Label(modal, text=title, font=("Segoe UI", 14, "bold"))
    lbl_title.pack(pady=(12, 4))

    lbl_meta = tk.Label(modal, text=f"Category: {category}    •    Risk: {risk}", font=("Segoe UI", 9, "italic"), fg="#666666")
    lbl_meta.pack()

    lbl_text = tk.Label(modal, text=description, justify="left", wraplength=480, font=("Segoe UI", 10))
    lbl_text.pack(padx=12, pady=(12, 10), expand=True)

    btn_frame = tk.Frame(modal)
    btn_frame.pack(pady=8)

    result = {"proceed": False}

    def on_continue() -> None:
        result["proceed"] = True
        modal.destroy()

    def on_cancel() -> None:
        result["proceed"] = False
        modal.destroy()

    btn_yes = tk.Button(btn_frame, text="Continue", bg="#007bff", fg="white", command=on_continue, width=12)
    btn_yes.pack(side="left", padx=8)
    btn_no = tk.Button(btn_frame, text="Cancel", command=on_cancel, width=12)
    btn_no.pack(side="left", padx=8)

    # Center the modal over parent and wait (modal)
    parent.update_idletasks()            # one-time geometry update to compute center
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    modal.update_idletasks()
    mx = parent_x + (parent_w - 520) // 2
    my = parent_y + (parent_h - 330) // 2
    modal.geometry(f"+{mx}+{my}")

    modal.wait_window()

    return result["proceed"]



class Spinner(tk.Label):
    """
    Spinner profissional usando 12 PNGs individuais.
    Os arquivos devem estar em: images/spinner/frame_0.png ... frame_11.png
    """

    def __init__(self, parent, folder="images/spinner", delay=80, size=64, debug=False):
        super().__init__(parent)
  # card fundo branco

        self.delay = delay
        self.frames = []
        self.index = 0
        self.debug = debug

        # Verifica pasta
        import os
        if not os.path.exists(folder):
            raise FileNotFoundError(f"Pasta do spinner não encontrada: {folder}")

        # Carrega frames
        for i in range(12):
            path = f"{folder}/frame_{i}.png"

            if not os.path.exists(path):
                raise FileNotFoundError(f"Frame não encontrado: {path}")

            img = Image.open(path).convert("RGBA")
            img = img.resize((size, size), Image.LANCZOS)

            # Torna o spinner visível — recolore para cinza escuro
            pixels = img.load()
            for x in range(img.width):
                for y in range(img.height):
                    r, g, b, a = pixels[x, y]
                    # só afeta pixels visíveis
                    if a > 0:
                        # cinza escuro
                        pixels[x, y] = (60, 60, 60, a)

            self.frames.append(ImageTk.PhotoImage(img))

        # Inicia animação
        self.after(self.delay, self.animate)

        self.after_id = None

        if self.debug:
            print(f"[Spinner] {len(self.frames)} frames carregados de '{folder}'")

    def animate(self):
        """Animação contínua."""
        if not self.frames:
            return

        # SE O WIDGET FOI DESTRUÍDO → PARE
        if not self.winfo_exists():
            return

        try:
            self.config(image=self.frames[self.index])
            self.index = (self.index + 1) % len(self.frames)

            # GUARDA O ID DO AFTER
            self.after_id = self.after(self.delay, self.animate)

        except tk.TclError:
            # widget destruído durante animação
            return


window = Window()