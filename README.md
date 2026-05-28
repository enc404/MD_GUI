# MarkItDown App

A cross-platform desktop application for converting files to Markdown, powered by Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library. Available for **Windows**, **Linux**, and **macOS**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Batch conversion** — convert multiple files at once
- **Folder scanning** — recursively find and convert all supported files in a directory
- **Dark themed UI** — modern, clean interface
- **Progress tracking** — real-time progress bar and detailed conversion log
- **Flexible output** — save to source directory or a custom output folder
- **Overwrite control** — optionally overwrite existing `.md` files

## Supported Formats

| Category | Formats |
|----------|---------|
| Documents | PDF, DOCX, PPTX |
| Spreadsheets | XLSX, XLS, CSV |
| Web | HTML, HTM |
| E-books | EPUB |
| Images | JPG, JPEG, PNG, GIF, BMP, TIFF, WebP |
| Audio | MP3, WAV, M4A, OGG |
| Notebooks | Jupyter (.ipynb) |
| Email | Outlook MSG |
| Archives | ZIP |
| Text | TXT, JSON, XML, YAML, RST, LOG |

## Quick Start

### Option 1: Run from Source

```bash
# Clone the repository
git clone https://github.com/enc404/markitdown-app.git
cd markitdown-app

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run the app
python -m markitdown_app.main
```

### Option 2: Build a Standalone Executable

**Windows:**
```cmd
build.bat
```

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

The executable will be created at `dist/MarkItDown.exe` (Windows) or `dist/MarkItDown` (Linux/macOS).

## Usage

1. **Add files** — Click "Add Files" to select individual files, or "Add Folder" to scan an entire directory
2. **Set output** — By default, `.md` files are saved next to the source file. Click "Browse" to choose a different output directory
3. **Configure** — Check "Overwrite existing .md files" if you want to replace previously converted files
4. **Convert** — Click "Convert to Markdown" to start the batch conversion
5. **Review** — Check the conversion log for results. Click "Open Output Folder" to view the generated files

### Keyboard Shortcuts

- `Delete` / `Backspace` — Remove selected file(s) from the list

## Project Structure

```
markitdown-app/
├── src/
│   └── markitdown_app/
│       ├── __init__.py       # Package metadata
│       ├── main.py           # Entry point
│       ├── app.py            # GUI application (tkinter)
│       └── converter.py      # MarkItDown wrapper & conversion logic
├── build.spec                # PyInstaller build configuration
├── build.bat                 # Windows build script
├── build.sh                  # Linux/macOS build script
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── LICENSE                   # MIT License
└── README.md
```

## Requirements

- Python 3.10 or later
- Dependencies (installed automatically):
  - [markitdown](https://github.com/microsoft/markitdown) — Microsoft's file-to-Markdown converter
  - [pyinstaller](https://pyinstaller.org/) — for building standalone executables

## License

MIT License — see [LICENSE](LICENSE) for details.

## Credits

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) — the core conversion engine
