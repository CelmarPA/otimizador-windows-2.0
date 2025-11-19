import tkinter as tk
from datetime import datetime


class LogPanel:

    def __init__(self, parent):
        # Create lateral frame for logs
        self.frame = tk.Frame(parent, bg="#1e1e1e")
        self.frame.grid(row=0, column=1, sticky="ns")

        # Title
        title = tk.Label(
            self.frame,
            text=" LOGS",
            fg="white",
            bg="#252526",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padx=10,
            pady=5
        )
        title.pack(fill="x")

        # Container for text + scrollbar
        text_frame = tk.Frame(self.frame, bg="#1e1e1e")
        text_frame.pack(fill="both", expand=True)

        # Custom scrollbar
        self.scrollbar = tk.Scrollbar(
            text_frame,
            orient="vertical",
            troughcolor="#1e1e1e",
            bg="#4e4e4e",
            activebackground="#6e6e6e",
            highlightthickness=0
        )
        self.scrollbar.pack(side="right", fill="y")

        # Text widget
        self.text_widget = tk.Text(
            text_frame,
            bg="#1e1e1e",
            fg="#dcdcdc",
            insertbackground="white",
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
            yscrollcommand=self.scrollbar.set
        )
        self.text_widget.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.text_widget.yview)

        # Color tags
        self.text_widget.tag_config("INFO", foreground="#60a5fa")  # blue
        self.text_widget.tag_config("SUCCESS", foreground="#4ade80")  # green
        self.text_widget.tag_config("ERROR", foreground="#f87171")  # red
        self.text_widget.tag_config("WARNING", foreground="#facc15")  # yellow
        self.text_widget.tag_config("TIME", foreground="#888") # dark brown

        # Block user editing
        self.text_widget.config(state=tk.DISABLED)

    def _insert(self, message, tag) -> None:
        """
        Inserts a message into the text widget.
        :param message:
        :param teg:
        :return: None
        """

        self.text_widget.config(state=tk.NORMAL)

        timestamp = datetime.now().strftime("[%H:%M:%S] ")

        self.text_widget.insert("end", timestamp, "TIME")
        self.text_widget.insert("end", message + "\n", tag)

        self.text_widget.see("end")
        self.text_widget.config(state=tk.DISABLED)

    def info(self, msg) -> None:
        self._insert(msg, "INFO")

    def success(self, msg) -> None:
        self._insert(msg, "SUCCESS")

    def error(self, msg) -> None:
        self._insert(msg, "ERROR")

    def warning(self, msg) -> None:
        self._insert(msg, "WARNING")

    def clear(self) -> None:
        """
        Clears the entire log.
        :return: None
        """

        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", "end")
        self.text_widget.config(state=tk.DISABLED)

    def log(self, message: str, tag="INFO"):
        self._insert(message, tag)