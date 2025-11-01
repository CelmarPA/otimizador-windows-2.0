from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import messagebox, PhotoImage
import webbrowser


class Window:
    
    def __init__(self, width: int = 600, height: int = 780) -> None:
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

        # Frame buttons
        self.button_frame = tk.Frame(self.container, bg="#ffffff")
        self.button_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)

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
            ("PC Performance Test", self.pc_performance_test, "#ff6b6b"),  # Red
            ("Disable SysMain", self.disable_sysmain, "#f5a623"),  # Orange
            ("Clean Temporary Files", self.clean_temporary_files, "#32cd32"),  # Green
            ("Enable High Performance Power Plan", self.enable_high_power_performance, "#007bff"),  # Blue
            ("Disable Background Apps", self.disable_background_apps, "#8e44ad"),  # Purple
            ("Enable Background Apps", self.enable_background_apps, "#20b2aa"),  # Teal
            ("Complete Optimization", self.complete_optimization, "#2c3e50"),  # Navy gray
            ("Update All Software", self.update_software, "#009688"),  # Cyan
            ("Windows / Office Activator / Repair", self.massgrave_activator, "#34495e")  # Dark gray
        ]

        # Loop to create and add each button
        for text, command, color in buttons:
            button = tk.Button(
                self.button_frame,
                text=text,
                command=command,
                height=2,
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

        # Criar máscara arredondada
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, *img.size), radius=radius, fill=255)

        # Criar background do mesmo tamanho
        background = Image.new("RGBA", img.size)
        background.paste(img, (0, 0), mask=mask)  # aplica a máscara no paste

        return ImageTk.PhotoImage(background)  # <- retorna o background, não img

    def on_enter(self, event: tk.Event) -> None:
        color = event.widget.original_bg
        darker = self.darken_color(color)
        event.widget["background"] = darker
        event.widget.config(font=("Segoe UI", 11, "bold"))
        event.widget.after(10, lambda: event.widget.config(height=3))

    def on_leave(self, event: tk.Event) -> None:
        event.widget["background"] = event.widget.original_bg
        event.widget.config(font=("Segoe UI", 10, "bold"))
        event.widget.after(10, lambda: event.widget.config(height=2))

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

    def pc_performance_test(self):
        messagebox.showinfo(title="Performance Test", message="Running Performance Test...")
        return None

    def disable_sysmain(self):
        messagebox.showinfo("Disable SysMain", "Disabling SysMain...")
        return None

    def disable_winsat(self):
        messagebox.showinfo("Disable WinSAT", "Disabling WinSAT...")
        return None

    def enable_high_power_performance(self):
        messagebox.showinfo("Enable High Performance", "Setting Power Plan to High Performance...")
        return None

    def clean_temporary_files(self):
        messagebox.showinfo("Clean Temporary Files", "Cleaning Temporary Files...")
        return None

    def disable_background_apps(self):
        messagebox.showinfo("Disable Background Apps", "Disabling Background Apps...")
        return None

    def enable_background_apps(self):
        messagebox.showinfo("Enable Background Apps", "Enabling Background Apps...")
        return None

    def complete_optimization(self):
        messagebox.showinfo("Full Optimization", "Performing Full Optimization...")
        return None

    def update_software(self):
        messagebox.showinfo("Update All Software", "Updating All Software...")
        return None

    def massgrave_activator(self):
        messagebox.showinfo("Activator / Troubleshoot", "Massgrave Activator...")
        return None



window = Window()