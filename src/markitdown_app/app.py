"""Main GUI application for MarkItDown file converter."""

import os
import platform
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from typing import Optional

from markitdown_app.converter import FileConverter, SUPPORTED_EXTENSIONS, ConversionResult


def _get_fonts() -> dict[str, str]:
    """Return platform-appropriate font families."""
    system = platform.system()
    if system == "Darwin":
        return {"ui": "SF Pro Text", "mono": "Menlo"}
    elif system == "Windows":
        return {"ui": "Segoe UI", "mono": "Consolas"}
    else:
        return {"ui": "DejaVu Sans", "mono": "DejaVu Sans Mono"}


_FONTS = _get_fonts()

# Color scheme
COLORS = {
    "bg": "#1e1e2e",
    "surface": "#282840",
    "surface_light": "#313150",
    "primary": "#7c3aed",
    "primary_hover": "#6d28d9",
    "success": "#10b981",
    "error": "#ef4444",
    "warning": "#f59e0b",
    "text": "#e2e8f0",
    "text_dim": "#94a3b8",
    "border": "#3b3b5c",
    "accent": "#818cf8",
}


class MarkItDownApp:
    """Main application window."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("MarkItDown — File to Markdown Converter")
        self.root.geometry("900x700")
        self.root.minsize(700, 550)
        self.root.configure(bg=COLORS["bg"])

        # Try to set icon (Windows only)
        try:
            self.root.iconbitmap(default="")
        except tk.TclError:
            pass

        self.converter = FileConverter()
        self.file_list: list[str] = []
        self.output_dir: Optional[str] = None
        self.is_converting = False
        self.overwrite_var = tk.BooleanVar(value=False)

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TFrame", background=COLORS["bg"])
        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=(_FONTS["ui"], 10),
        )
        style.configure(
            "Title.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=(_FONTS["ui"], 18, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text_dim"],
            font=(_FONTS["ui"], 10),
        )
        style.configure(
            "Section.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=(_FONTS["ui"], 11, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text_dim"],
            font=(_FONTS["ui"], 9),
        )
        style.configure(
            "Success.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["success"],
            font=(_FONTS["ui"], 9),
        )
        style.configure(
            "Error.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["error"],
            font=(_FONTS["ui"], 9),
        )

        # Buttons
        style.configure(
            "Primary.TButton",
            background=COLORS["primary"],
            foreground="white",
            font=(_FONTS["ui"], 10, "bold"),
            padding=(16, 8),
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORS["primary_hover"]), ("disabled", COLORS["surface_light"])],
            foreground=[("disabled", COLORS["text_dim"])],
        )
        style.configure(
            "Secondary.TButton",
            background=COLORS["surface_light"],
            foreground=COLORS["text"],
            font=(_FONTS["ui"], 10),
            padding=(12, 6),
            borderwidth=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", COLORS["border"])],
        )
        style.configure(
            "Danger.TButton",
            background=COLORS["error"],
            foreground="white",
            font=(_FONTS["ui"], 10),
            padding=(12, 6),
            borderwidth=0,
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#dc2626")],
        )

        # Progressbar
        style.configure(
            "Custom.Horizontal.TProgressbar",
            background=COLORS["primary"],
            troughcolor=COLORS["surface"],
            borderwidth=0,
            thickness=6,
        )

        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=(_FONTS["ui"], 10),
        )
        style.map(
            "TCheckbutton",
            background=[("active", COLORS["bg"])],
        )

    def _build_ui(self) -> None:
        # Main container with padding
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main)
        header.pack(fill=tk.X, pady=(0, 16))
        ttk.Label(header, text="MarkItDown", style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Label(
            header,
            text="Convert files to Markdown using Microsoft's MarkItDown",
            style="Subtitle.TLabel",
        ).pack(side=tk.LEFT, padx=(12, 0), pady=(6, 0))

        # Separator
        sep = tk.Frame(main, height=1, bg=COLORS["border"])
        sep.pack(fill=tk.X, pady=(0, 16))

        # Top section: file selection + output
        top_frame = ttk.Frame(main)
        top_frame.pack(fill=tk.X, pady=(0, 8))

        # File selection buttons
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Label(btn_frame, text="Input Files", style="Section.TLabel").pack(
            side=tk.LEFT, padx=(0, 16)
        )

        ttk.Button(
            btn_frame, text="Add Files", command=self._add_files, style="Secondary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(
            btn_frame, text="Add Folder", command=self._add_folder, style="Secondary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(
            btn_frame, text="Clear All", command=self._clear_files, style="Danger.TButton"
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.file_count_label = ttk.Label(btn_frame, text="0 files", style="Status.TLabel")
        self.file_count_label.pack(side=tk.RIGHT)

        # File list
        list_frame = ttk.Frame(main)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 8))

        # Listbox with scrollbar
        self.file_listbox = tk.Listbox(
            list_frame,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            selectbackground=COLORS["primary"],
            selectforeground="white",
            font=(_FONTS["mono"], 10),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=COLORS["border"],
            highlightbackground=COLORS["border"],
            activestyle="none",
        )
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)

        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Placeholder text
        self._show_placeholder()

        # Bind delete key to remove selected
        self.file_listbox.bind("<Delete>", lambda e: self._remove_selected())
        self.file_listbox.bind("<BackSpace>", lambda e: self._remove_selected())

        # Output directory selection
        out_frame = ttk.Frame(main)
        out_frame.pack(fill=tk.X, pady=(8, 4))

        ttk.Label(out_frame, text="Output Directory", style="Section.TLabel").pack(
            side=tk.LEFT, padx=(0, 12)
        )

        self.output_label = ttk.Label(
            out_frame, text="Same as source file", style="Status.TLabel"
        )
        self.output_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            out_frame,
            text="Browse",
            command=self._select_output_dir,
            style="Secondary.TButton",
        ).pack(side=tk.RIGHT, padx=(6, 0))

        ttk.Button(
            out_frame,
            text="Reset",
            command=self._reset_output_dir,
            style="Secondary.TButton",
        ).pack(side=tk.RIGHT)

        # Options
        opt_frame = ttk.Frame(main)
        opt_frame.pack(fill=tk.X, pady=(4, 8))

        ttk.Checkbutton(
            opt_frame,
            text="Overwrite existing .md files",
            variable=self.overwrite_var,
        ).pack(side=tk.LEFT)

        # Supported formats info
        formats_text = "Supported: PDF, DOCX, PPTX, XLSX, XLS, CSV, HTML, EPUB, Images, Audio, Jupyter, MSG, ZIP, TXT"
        ttk.Label(opt_frame, text=formats_text, style="Status.TLabel").pack(side=tk.RIGHT)

        # Progress bar
        self.progress = ttk.Progressbar(
            main,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar",
        )
        self.progress.pack(fill=tk.X, pady=(4, 4))

        # Status line
        status_frame = ttk.Frame(main)
        status_frame.pack(fill=tk.X, pady=(0, 4))

        self.status_label = ttk.Label(status_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT)

        self.result_label = ttk.Label(status_frame, text="", style="Status.TLabel")
        self.result_label.pack(side=tk.RIGHT)

        # Log area
        log_frame = ttk.Frame(main)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        ttk.Label(log_frame, text="Conversion Log", style="Section.TLabel").pack(
            anchor=tk.W, pady=(0, 4)
        )

        self.log_text = tk.Text(
            log_frame,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(_FONTS["mono"], 9),
            height=6,
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=COLORS["border"],
            highlightbackground=COLORS["border"],
            wrap=tk.WORD,
            state=tk.DISABLED,
        )
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure log tags
        self.log_text.tag_configure("success", foreground=COLORS["success"])
        self.log_text.tag_configure("error", foreground=COLORS["error"])
        self.log_text.tag_configure("warning", foreground=COLORS["warning"])
        self.log_text.tag_configure("info", foreground=COLORS["accent"])

        # Convert button (bottom)
        bottom_frame = ttk.Frame(main)
        bottom_frame.pack(fill=tk.X, pady=(4, 0))

        self.convert_btn = ttk.Button(
            bottom_frame,
            text="Convert to Markdown",
            command=self._start_conversion,
            style="Primary.TButton",
        )
        self.convert_btn.pack(side=tk.RIGHT)

        # Open output folder button (hidden initially)
        self.open_output_btn = ttk.Button(
            bottom_frame,
            text="Open Output Folder",
            command=self._open_output_folder,
            style="Secondary.TButton",
        )

    def _show_placeholder(self) -> None:
        self.file_listbox.insert(tk.END, "  Drag & drop files here, or use 'Add Files' / 'Add Folder'")
        self.file_listbox.itemconfig(0, fg=COLORS["text_dim"])

    def _clear_placeholder(self) -> None:
        if self.file_listbox.size() == 1:
            item = self.file_listbox.get(0)
            if "Drag" in item or "Add Files" in item:
                self.file_listbox.delete(0, tk.END)

    def _add_files(self) -> None:
        filetypes = [
            ("All Supported Files", " ".join(f"*{ext}" for ext in sorted(SUPPORTED_EXTENSIONS.keys()))),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("PowerPoint", "*.pptx"),
            ("Excel Files", "*.xlsx *.xls"),
            ("CSV Files", "*.csv"),
            ("HTML Files", "*.html *.htm"),
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp"),
            ("E-books", "*.epub"),
            ("Jupyter Notebooks", "*.ipynb"),
            ("All Files", "*.*"),
        ]
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=filetypes,
        )
        if files:
            self._clear_placeholder()
            added = 0
            for f in files:
                if f not in self.file_list:
                    self.file_list.append(f)
                    self.file_listbox.insert(tk.END, f"  {f}")
                    added += 1
            self._update_file_count()
            if added:
                self._log(f"Added {added} file(s)", "info")

    def _add_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select folder to scan for convertible files")
        if not folder:
            return

        self._clear_placeholder()
        added = 0
        for root, _, files in os.walk(folder):
            for fname in sorted(files):
                fpath = os.path.join(root, fname)
                ext = Path(fpath).suffix.lower()
                if ext in SUPPORTED_EXTENSIONS and fpath not in self.file_list:
                    self.file_list.append(fpath)
                    self.file_listbox.insert(tk.END, f"  {fpath}")
                    added += 1

        self._update_file_count()
        if added:
            self._log(f"Added {added} file(s) from {folder}", "info")
        else:
            self._log(f"No supported files found in {folder}", "warning")

    def _clear_files(self) -> None:
        self.file_list.clear()
        self.file_listbox.delete(0, tk.END)
        self._show_placeholder()
        self._update_file_count()

    def _remove_selected(self) -> None:
        selection = self.file_listbox.curselection()
        if not selection:
            return
        for idx in reversed(selection):
            if idx < len(self.file_list):
                self.file_list.pop(idx)
                self.file_listbox.delete(idx)
        self._update_file_count()

    def _update_file_count(self) -> None:
        count = len(self.file_list)
        self.file_count_label.configure(text=f"{count} file{'s' if count != 1 else ''}")

    def _select_output_dir(self) -> None:
        d = filedialog.askdirectory(title="Select output directory")
        if d:
            self.output_dir = d
            display = d if len(d) <= 60 else "..." + d[-57:]
            self.output_label.configure(text=display)

    def _reset_output_dir(self) -> None:
        self.output_dir = None
        self.output_label.configure(text="Same as source file")

    def _log(self, message: str, tag: str = "") -> None:
        self.log_text.configure(state=tk.NORMAL)
        if tag:
            self.log_text.insert(tk.END, message + "\n", tag)
        else:
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _start_conversion(self) -> None:
        if self.is_converting:
            return

        if not self.file_list:
            messagebox.showwarning("No Files", "Please add files to convert first.")
            return

        self.is_converting = True
        self.convert_btn.configure(state=tk.DISABLED)
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.file_list)
        self.status_label.configure(text="Converting...", style="Status.TLabel")
        self.result_label.configure(text="")
        self.open_output_btn.pack_forget()

        # Clear log
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

        self._log(f"Starting conversion of {len(self.file_list)} file(s)...", "info")

        # Run conversion in background thread
        thread = threading.Thread(target=self._convert_files, daemon=True)
        thread.start()

    def _convert_files(self) -> None:
        success_count = 0
        fail_count = 0
        total = len(self.file_list)

        for i, file_path in enumerate(self.file_list):
            filename = Path(file_path).name
            self.root.after(0, lambda fn=filename, idx=i: self._update_status(fn, idx, total))

            result = self.converter.convert_file(
                file_path,
                output_dir=self.output_dir,
                overwrite=self.overwrite_var.get(),
            )

            if result.success:
                success_count += 1
                self.root.after(
                    0,
                    lambda r=result: self._log(
                        f"  OK  {Path(r.source_path).name} -> {Path(r.output_path).name}",
                        "success",
                    ),
                )
            else:
                fail_count += 1
                self.root.after(
                    0,
                    lambda r=result: self._log(
                        f"  FAIL  {Path(r.source_path).name}: {r.error_message}",
                        "error",
                    ),
                )

            self.root.after(0, lambda v=i + 1: self._update_progress(v))

        self.root.after(0, lambda: self._conversion_done(success_count, fail_count, total))

    def _update_status(self, filename: str, idx: int, total: int) -> None:
        self.status_label.configure(text=f"Converting ({idx + 1}/{total}): {filename}")

    def _update_progress(self, value: int) -> None:
        self.progress["value"] = value

    def _conversion_done(self, success: int, fail: int, total: int) -> None:
        self.is_converting = False
        self.convert_btn.configure(state=tk.NORMAL)

        self._log(f"\nDone: {success} succeeded, {fail} failed out of {total} total.", "info")

        if fail == 0:
            self.status_label.configure(text="All conversions completed successfully!", style="Success.TLabel")
        elif success == 0:
            self.status_label.configure(text="All conversions failed.", style="Error.TLabel")
        else:
            self.status_label.configure(text=f"Completed with {fail} error(s).", style="Status.TLabel")

        self.result_label.configure(text=f"{success}/{total} converted")

        # Show open output folder button
        self.open_output_btn.pack(side=tk.LEFT)

    def _open_output_folder(self) -> None:
        target = self.output_dir
        if not target and self.file_list:
            target = str(Path(self.file_list[0]).parent)

        if target:
            if sys.platform == "win32":
                os.startfile(target)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                os.system(f'open "{target}"')
            else:
                os.system(f'xdg-open "{target}"')

    def run(self) -> None:
        self.root.mainloop()
