import tkinter as tk
from tkinter import messagebox


class Window:
    
    def __init__(self, width: int = 600, height: int = 650):
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

        # Central container (card)
        self.container = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.container.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)

        # Frame buttons
        self.button_frame = tk.Frame(self.container, bg="#ffffff")
        self.button_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)

        # Create the main menu buttons.
        self.create_buttons()

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
            bg="#1e90ff",
            fg="white",
            padx=10,
            pady=10
        )
        title_label.pack(fill=tk.X)

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

    def on_enter(self, event: tk.Event) -> None:
        color = event.widget.original_bg
        darker = self.darken_color(color)
        event.widget["background"] = darker

    def on_leave(self, event: tk.Event) -> None:
        event.widget["background"] = event.widget.original_bg

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