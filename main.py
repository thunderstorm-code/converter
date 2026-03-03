from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from teva_ui import TevaWindow


class ConverterService:
    """Simple file conversion service.

    Uses Pillow when available for image conversion. If Pillow is missing,
    conversion gracefully falls back with a clear error.
    """

    supported_inputs = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    def convert_one(self, input_path: str, target_ext: str, quality: int) -> Path:
        src = Path(input_path)
        if not src.exists() or not src.is_file():
            raise ValueError("Файл не найден")
        if src.suffix.lower() not in self.supported_inputs:
            raise ValueError("Неподдерживаемый тип исходного файла")

        dst = src.with_suffix(f".{target_ext.lower()}")
        self._save_image(src, dst, quality)
        return dst

    def convert_folder(self, folder_path: str, target_ext: str, quality: int) -> int:
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            raise ValueError("Папка не найдена")

        files = [p for p in folder.iterdir() if p.suffix.lower() in self.supported_inputs]
        if not files:
            raise ValueError("В папке нет подходящих файлов")

        for src in files:
            dst = src.with_suffix(f".{target_ext.lower()}")
            self._save_image(src, dst, quality)
        return len(files)

    def _save_image(self, src: Path, dst: Path, quality: int) -> None:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Для конвертации нужен Pillow: pip install pillow") from exc

        with Image.open(src) as img:
            img.save(dst, quality=quality)


class TevaController:
    def __init__(self, window: TevaWindow, service: ConverterService) -> None:
        self.window = window
        self.service = service

        self.window.convert_requested.connect(self.handle_single_convert)
        self.window.batch_requested.connect(self.handle_batch_convert)

    def handle_single_convert(self, path: str, fmt: str, quality: int) -> None:
        try:
            result = self.service.convert_one(path, fmt, quality)
            self.window.set_single_status(f"Готово: {result.name}")
        except Exception as exc:
            self.window.set_single_status(f"Ошибка: {exc}", error=True)

    def handle_batch_convert(self, path: str, fmt: str, quality: int) -> None:
        try:
            count = self.service.convert_folder(path, fmt, quality)
            self.window.set_batch_status(f"Готово: обработано {count} файлов")
        except Exception as exc:
            self.window.set_batch_status(f"Ошибка: {exc}", error=True)


def main() -> None:
    app = QApplication(sys.argv)
    win = TevaWindow()
    TevaController(win, ConverterService())
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
