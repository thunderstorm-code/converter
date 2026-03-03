from __future__ import annotations

from pathlib import Path

import eel


class КонвертерСервис:
    поддержка = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    def конвертировать_файл(self, путь_к_файлу: str, формат: str, качество: int) -> str:
        исходник = Path(путь_к_файлу.strip())
        if not исходник.exists() or not исходник.is_file():
            raise ValueError("Файл не найден")
        if исходник.suffix.lower() not in self.поддержка:
            raise ValueError("Неподдерживаемый исходный формат")

        формат = формат.lower().strip().replace('.', '')
        результат = исходник.with_suffix(f".{формат}")
        self._сохранить_картинку(исходник, результат, качество)
        return str(результат)

    def конвертировать_папку(self, путь_к_папке: str, формат: str, качество: int) -> int:
        папка = Path(путь_к_папке.strip())
        if not папка.exists() or not папка.is_dir():
            raise ValueError("Папка не найдена")

        файлы = [p for p in папка.iterdir() if p.suffix.lower() in self.поддержка]
        if not файлы:
            raise ValueError("В папке нет подходящих изображений")

        формат = формат.lower().strip().replace('.', '')
        for исходник in файлы:
            результат = исходник.with_suffix(f".{формат}")
            self._сохранить_картинку(исходник, результат, качество)
        return len(файлы)

    def _сохранить_картинку(self, исходник: Path, результат: Path, качество: int) -> None:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Нужен Pillow: pip install pillow") from exc

        with Image.open(исходник) as img:
            if результат.suffix.lower() in {".jpg", ".jpeg"} and img.mode in {"RGBA", "LA", "P"}:
                img = img.convert("RGB")
            img.save(результат, quality=int(качество))


сервис = КонвертерСервис()


@eel.expose
def конвертировать_один(путь_к_файлу: str, формат: str, качество: int) -> dict:
    try:
        результат = сервис.конвертировать_файл(путь_к_файлу, формат, качество)
        return {"ok": True, "message": f"Готово: {результат}"}
    except Exception as e:
        return {"ok": False, "message": f"Ошибка: {e}"}


@eel.expose
def конвертировать_пачку(путь_к_папке: str, формат: str, качество: int) -> dict:
    try:
        количество = сервис.конвертировать_папку(путь_к_папке, формат, качество)
        return {"ok": True, "message": f"Готово: обработано {количество} файлов"}
    except Exception as e:
        return {"ok": False, "message": f"Ошибка: {e}"}


def main() -> None:
    eel.init("web")
    eel.start("index.html", size=(1000, 700), title="Teva")


if __name__ == "__main__":
    main()
