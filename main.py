import time
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import webbrowser
from system_actions import SystemActions
from log_panel import LogPanel


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

    def create_buttons(self) -> None:
        """
        It creates the main menu buttons and arranges them vertically.

        :return: None
        """

        # List of buttons: (Button text, function called)
        buttons = [
            ("PC Performance Test", self.actions.pc_performance_test, "#ff6b6b"),  # Red
            ("Create Restore Point", self.actions.create_restore_point, "#34495e"), # Dark gray
            ("Enable / Disable SysMain", lambda: self.toggle_service_with_overlay("SysMain", "SysMain / SuperFetch"), "#f5a623"),  # Orange
            ("Clean Temporary Files", self.actions.clean_temporary_files, "#32cd32"),  # Green
            ("Deep Cleaning", self.actions.start_cleanup, "#4b0082"),  # Green
            ("Enable High Performance Power Plan", self.actions.enable_high_power_plan, "#007bff"),  # Blue
            ("Disable Background Apps", self.actions.disable_background_apps, "#8e44ad"),  # Purple
            ("Complete Optimization", self.actions.complete_optimization, "#2c3e50"),  # Navy gray
            ("Update All Software", self.actions.update_software, "#009688"),  # Cyan
            ("Enable / Disable Windows Update", lambda: self.toggle_service_with_overlay("wuauserv", "Windows Update Service"), "#2980b9"),
            ("Enable / Disable BITS", lambda: self.toggle_service_with_overlay("bits", "Background Intelligent Transfer Service"), "#9b59b6"),
            ("Enable / Disable Print Spooler", lambda: self.toggle_service_with_overlay("spooler", "Print Spooler"), "#e67e22"),
            ("Enable / Disable Windows Search", lambda: self.toggle_service_with_overlay("wsearch", "Windows Search Indexing"), "#16a085"),
            ("Windows / Office Activator / Repair", self.actions.massgrave_activator, "#34495e")  # Dark gray
        ]

        # Loop to create and add each button
        for text, command, color in buttons:
            button = tk.Button(
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
            button.original_bg = color
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)
            button.pack(pady=8, fill=tk.X)

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

    def run_action(self, func, label):
        func()

    # Integration helper in main window class
    # Inside your Window class (or wherever you create buttons), add a method like this:
    def toggle_service_with_overlay(self, service_name: str, friendly_name: str) -> None:
        """
        Full flow:
        - Show explanation modal
        - Detect current state
        - Show overlay
        - Call backend async toggle
        - Update logs + UI
        """

        # Explanation
        proceed = show_service_info(self.root, service_name, friendly_name)

        if not proceed:
            if self.log_panel:
                self.log_panel.info("User cancelled service operation.")

            return

        # Check state quickly
        status = self.actions._check_service_status(service_name)  # uses backend helper

        if status == "running":
            action = "disable"
            verb = "Disabling"

        else:
            action = "enable"
            verb = "Enabling"

        # Overlay
        overlay = ProgressOverlay(
            self.root,
            title=f"{verb} {friendly_name}...",
            message=f"{verb} {friendly_name}. Please wait."
        )

        if self.log_panel:
            self.log_panel.info(f"▶️ {verb} {friendly_name}...")

        # Callbacks
        def on_start() -> None:
            overlay.update_status(f"{verb}...")

        def on_finish(success, stderr) -> None:
            try:
                if success:
                    overlay.update_status("Done!")
                    time.sleep(0.6)
                    overlay.close()

                    if self.log_panel:
                        self.log_panel.success(f"{friendly_name} {action}d successfully.")

                    messagebox.showinfo("Success", f"{friendly_name} updated successfully.")

                else:
                    overlay.update_status("Failed")
                    time.sleep(0.6)
                    overlay.close()
                    if self.log_panel:
                        self.log_panel.error(f"{friendly_name} toggle failed: {stderr}")

                    messagebox.showerror("Error", f"Operation failed:\n{stderr}")


            except Exception as e:
                overlay.close()
                self.log_panel.error(f"Finish callback exception: {e}")

        def on_error(exc):
            overlay.update_status("Error")
            time.sleep(0.5)
            overlay.close()

            if self.log_panel:
                self.log_panel.error(f"Exception: {exc}")

            messagebox.showerror("Error", f"Exception: {exc}")

        # Run async task from system_actions.py
        self.actions.toggle_service_async(
            service_name=service_name,
            action=action,
            on_start=on_start,
            on_finish=on_finish,
            on_error=on_error
        )


class ProgressOverlay:

    def __init__(self,  parent: tk.Tk, title: str = "Working...", message: str = "") -> None:
        self.parent = parent

        # create a top-level full-screen overlay on top of parent window
        self.win = tk.Toplevel(parent)
        self.win.transient(parent)
        self.win.overrideredirect(True)  # remove borders

        # make it cover the parent window exactly
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        # ensure geometry updated
        parent.update_idletasks()
        self.win.geometry(f"{pw}x{ph}+{px}+{py}")

        # semi-transparent dark background
        self.bg = tk.Frame(self.win, bg="#000000")
        self.bg.place(relwidth=1.0, relheight=1.0)

        try:
            self.win.attributes("-alpha", 0.55)

        except Exception:
            # some platforms may not accept alpha on Toplevel
            pass

        # central card
        card_w, card_h = 420, 140
        cx = (pw - card_w) // 2
        cy = (ph - card_h) // 2
        self.card = tk.Frame(self.win, bg="#ffffff", bd=2, relief="raised")
        self.card.place(x=cx, y=cy, width=card_w, height=card_h)

        self.title_lbl = tk.Label(self.card, text=title, font=("Segoe UI", 12, "bold"), bg="#ffffff")
        self.title_lbl.pack(pady=(12, 6))

        self.msg_lbl = tk.Label(self.card, text=message, font=("Segoe UI", 10), bg="#ffffff", wraplength=380,
                                justify="center")
        self.msg_lbl.pack(pady=(0, 8))

        # Progress bar
        self.pb = ttk.Progressbar(self.card, mode="indeterminate", length=320)
        self.pb.pack(pady=(4, 8))
        self.pb.start()

        # Status
        self.status_lbl = tk.Label(self.card, text="Starting...", font=("Segoe UI", 9), bg="#ffffff")
        self.status_lbl.pack()

        # Allow manual close? no, hide window close
        self.win.protocol("WM_DELETE_WINDOW", lambda: None)

    def update_status(self, text: str) -> None:
        self.status_lbl.config(text=text)

        # Ensure new text is visible
        self.win.update_idletasks()

    def close(self):
        try:
            self.pb.stop()
        except Exception:
            pass

        try:
            self.win.destroy()
        except Exception:
            pass


# Service explanation dialog
def show_service_info(parent: tk.Tk, service_name: str, friendly_name: str) -> bool:
    """
   Show a stylized explanation modal and return True if user wants to continue.
   """

    # Custom modal window
    modal = tk.Toplevel(parent)
    modal.transient(parent)
    modal.grab_set()
    modal.title(f"{friendly_name} ({service_name})")
    modal.geometry("520x300")
    modal.resizable(False, False)

    # Title
    lbl_title = tk.Label(modal, text=f"{friendly_name}",font=("Segoe UI", 14, "bold"))
    lbl_title.pack(pady=(12, 8))

    # Explanatory text (tailor per service)
    explanation = (
        f"The service '{friendly_name}' (service name: {service_name}) helps Windows optimize app loading and system responsiveness.\n\n"
        "Notes:\n"
        "- Formerly known as SuperFetch.\n"
        "- May improve launch times for frequently used apps.\n"
        "- On HDDs can cause high disk activity; on SSDs it's usually unnecessary.\n\n"
        "Do you want to continue and toggle this service?"
    )

    lbl_text = tk.Label(modal, text=explanation, justify="left", wraplength=480)
    lbl_text.pack(padx=12, pady=(0, 10), expand=True)

    # Buttons
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

    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    patent_w = parent.winfo_width()
    patent_h = parent.winfo_height()

    # Center Modal
    modal.update_idletasks()
    mx = parent_x + (patent_w - 520) // 2
    my = parent_y + (patent_h - 300) // 2
    modal.geometry(f"+{mx}+{my}")

    modal.wait_window()

    return result["proceed"]








window = Window()