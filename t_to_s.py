from __future__ import annotations

from pathlib import Path


def convert_tdata_to_telethon(tdata_dir: str, output_session_path: str) -> str:
    source_dir = Path(tdata_dir).expanduser().resolve()
    session_path = Path(output_session_path).expanduser().resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError("tdata directory was not found")

    session_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from opentele.td import TDesktop
        from opentele.api import API
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: install opentele to convert tdata -> telethon"
        ) from exc

    async def _run() -> str:
        desktop = TDesktop(str(source_dir), api=API.TelegramDesktop)
        client = await desktop.ToTelethon(session=str(session_path), flag=CreateNewSession, api=API.TelegramDesktop)
        await client.connect()
        await client.disconnect()
        return str(session_path)

    from opentele.tl import CreateNewSession
    import asyncio

    return asyncio.run(_run())
