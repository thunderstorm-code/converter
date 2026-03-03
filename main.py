from __future__ import annotations

from pathlib import Path

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

    def tdata_to_telethon(self, tdata_dir: str, output_session_path: str) -> str:
        if not tdata_dir.strip():
            raise ValueError("tdata path is required")
        if not output_session_path.strip():
            raise ValueError("Output session path is required")
        return convert_tdata_to_telethon(tdata_dir, output_session_path)


service = TgConverterService()


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
            output_session_path=data.get("outputSessionPath", ""),
        )
        return {"ok": True, "message": f"Done: {result}"}
    except Exception as exc:
        return {"ok": False, "message": f"Error: {exc}"}


def main() -> None:
    eel.init("web")
    eel.start("index.html", size=(1080, 760), title="Teva TG Converter")


if __name__ == "__main__":
    main()
