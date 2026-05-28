"""Core conversion logic wrapping Microsoft's MarkItDown library."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from markitdown import MarkItDown


SUPPORTED_EXTENSIONS = {
    # Documents
    ".pdf": "PDF Document",
    ".docx": "Word Document",
    ".pptx": "PowerPoint Presentation",
    ".xlsx": "Excel Spreadsheet",
    ".xls": "Excel Spreadsheet (Legacy)",
    # Data
    ".csv": "CSV File",
    ".ipynb": "Jupyter Notebook",
    # Web
    ".html": "HTML File",
    ".htm": "HTML File",
    # Media
    ".jpg": "JPEG Image",
    ".jpeg": "JPEG Image",
    ".png": "PNG Image",
    ".gif": "GIF Image",
    ".bmp": "BMP Image",
    ".tiff": "TIFF Image",
    ".tif": "TIFF Image",
    ".webp": "WebP Image",
    ".mp3": "MP3 Audio",
    ".wav": "WAV Audio",
    ".m4a": "M4A Audio",
    ".ogg": "OGG Audio",
    # E-books
    ".epub": "EPUB E-book",
    # Email
    ".msg": "Outlook Message",
    # Archives
    ".zip": "ZIP Archive",
    # Text
    ".txt": "Plain Text",
    ".json": "JSON File",
    ".xml": "XML File",
    ".yaml": "YAML File",
    ".yml": "YAML File",
    ".rst": "reStructuredText",
    ".log": "Log File",
}


@dataclass
class ConversionResult:
    source_path: str
    output_path: Optional[str]
    success: bool
    error_message: Optional[str] = None
    markdown_content: Optional[str] = None


class FileConverter:
    """Wraps MarkItDown to convert files to Markdown."""

    def __init__(self) -> None:
        self._md = MarkItDown()

    def is_supported(self, file_path: str) -> bool:
        ext = Path(file_path).suffix.lower()
        return ext in SUPPORTED_EXTENSIONS

    def convert_file(
        self,
        source_path: str,
        output_dir: Optional[str] = None,
        overwrite: bool = False,
    ) -> ConversionResult:
        source = Path(source_path)

        if not source.exists():
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                error_message=f"File not found: {source_path}",
            )

        if not source.is_file():
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                error_message=f"Not a file: {source_path}",
            )

        # Determine output path
        if output_dir:
            out_dir = Path(output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
        else:
            out_dir = source.parent

        output_path = out_dir / (source.stem + ".md")

        if output_path.exists() and not overwrite:
            return ConversionResult(
                source_path=source_path,
                output_path=str(output_path),
                success=False,
                error_message=f"Output file already exists: {output_path}",
            )

        try:
            result = self._md.convert(str(source))
            markdown_text = result.text_content

            if not markdown_text or not markdown_text.strip():
                return ConversionResult(
                    source_path=source_path,
                    output_path=str(output_path),
                    success=False,
                    error_message="Conversion produced empty output",
                )

            output_path.write_text(markdown_text, encoding="utf-8")

            return ConversionResult(
                source_path=source_path,
                output_path=str(output_path),
                success=True,
                markdown_content=markdown_text,
            )

        except Exception as e:
            return ConversionResult(
                source_path=source_path,
                output_path=None,
                success=False,
                error_message=str(e),
            )

    def get_supported_extensions_filter(self) -> str:
        """Return a file dialog filter string for supported file types."""
        all_exts = " ".join(f"*{ext}" for ext in sorted(SUPPORTED_EXTENSIONS.keys()))
        filters = f"All Supported Files ({all_exts})"

        categories: dict[str, list[str]] = {}
        for ext, desc in SUPPORTED_EXTENSIONS.items():
            categories.setdefault(desc, []).append(ext)

        for desc, exts in sorted(categories.items()):
            ext_str = " ".join(f"*{e}" for e in sorted(exts))
            filters += f"|{desc} ({ext_str})"

        filters += "|All Files (*.*)"
        return filters
