import asyncio
import importlib
import random
import sys
import os
from telethon.sync import TelegramClient
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession, CreateNewSession

async def session_to_tdata(session_path):
    client = TelegramClient(session_path)
    tdesk = await client.ToTDesktop(flag=UseCurrentSession)
    tdesk.SaveTData(f"from_session_to_tdata/tdatas/{os.path.basename(session_path)}/tdata")

async def convert_session_to_tdata():
    for session in sessions:
        try:
            session_path = os.path.join('./from_session_to_tdata/sessions', session)
            await session_to_tdata(session_path)
            print(f'конвертирую session {session} в формат TData')
        except Exception as e:
            print(f'Произошла ошибка - {e}')

    print('Завершил конвертацию')
