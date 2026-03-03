from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import eel

from s_to_y import convert_telethon_to_tdata
from t_to_s import convert_tdata_to_telethon


class TgConverterService:
    def telethon_to_tdata(self, session_path: str, output_dir: str) -> str:
        if not session_path.strip():
            raise ValueError("Session path is required")
        if not output_dir.strip():
            raise ValueError("Output folder is required")
        return convert_telethon_to_tdata(session_path, output_dir)

    def tdata_to_telethon(self, tdata_dir: str, output_dir: str) -> str:
        if not tdata_dir.strip():
            raise ValueError("tdata folder is required")
        if not output_dir.strip():
            raise ValueError("Output folder is required")
        output_path = str(Path(output_dir).expanduser().resolve() / "converted.session")
        return convert_tdata_to_telethon(tdata_dir, output_path)


service = TgConverterService()


def _pick_file(title: str, filetypes: list[tuple[str, str]] | None = None) -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title=title, filetypes=filetypes or [("All files", "*.*")])
    root.destroy()
    return path or ""


def _pick_folder(title: str) -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askdirectory(title=title)
    root.destroy()
    return path or ""


@eel.expose
def pick_session_file() -> dict:
    path = _pick_file("Select Telethon session", [("Session files", "*.session"), ("All files", "*.*")])
    return {"path": path, "name": Path(path).name if path else ""}


@eel.expose
def pick_tdata_folder() -> dict:
    path = _pick_folder("Select tdata folder")
    return {"path": path, "name": Path(path).name if path else ""}


@eel.expose
def pick_output_folder() -> dict:
    path = _pick_folder("Select output folder")
    return {"path": path, "name": Path(path).name if path else ""}


@eel.expose
def convert_telethon(data: dict) -> dict:
    try:
        result = service.telethon_to_tdata(
            session_path=data.get("sessionPath", ""),
            output_dir=data.get("outputDir", ""),
        )
        return {"ok": True, "message": f"Done: {result}"}
    except Exception as exc:
        return {"ok": False, "message": f"Error: {exc}"}


@eel.expose
def convert_tdata(data: dict) -> dict:
    try:
        result = service.tdata_to_telethon(
            tdata_dir=data.get("tdataDir", ""),
            output_dir=data.get("outputDir", ""),
        )
        return {"ok": True, "message": f"Done: {result}"}
    except Exception as exc:
        return {"ok": False, "message": f"Error: {exc}"}


def main() -> None:
    eel.init("web")
    eel.start("index.html", size=(980, 700), title="Teva")


if __name__ == "__main__":
    main()
