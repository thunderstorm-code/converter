from __future__ import annotations

from pathlib import Path


def convert_telethon_to_tdata(session_path: str, output_dir: str) -> str:
    session_file = Path(session_path).expanduser().resolve()
    target_dir = Path(output_dir).expanduser().resolve()

    if not session_file.exists() or not session_file.is_file():
        raise ValueError("Telethon session file was not found")

    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        from opentele.td import TDesktop
        from opentele.api import API
        from opentele.tl import TelegramClient
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: install opentele to convert telethon -> tdata"
        ) from exc

    client = TelegramClient(str(session_file), api=API.TelegramDesktop)

    async def _run() -> str:
        await client.connect()
        if not await client.is_user_authorized():
            raise RuntimeError("Session is not authorized")

        desktop = await client.ToTDesktop(flag=TDesktop.Flag.CreateNewSession, api=API.TelegramDesktop)
        desktop.SaveTData(str(target_dir))
        await client.disconnect()
        return str(target_dir)

    import asyncio

    return asyncio.run(_run())
