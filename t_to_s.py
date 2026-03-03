import os
import asyncio
import uuid

from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession, CreateNewSession


async def tdata_to_session_telethon(tdata_folder, output_dir, new_session=False, password=None):
    try:
        tdesk = TDesktop(tdata_folder)

        session_name = os.path.basename(tdata_folder)
        uniq_id = uuid.uuid4()
        session_file = os.path.join(output_dir, f"{session_name}_{uniq_id}.session")

        api = API.TelegramIOS.Generate()
        client = await tdesk.ToTelethon(session_file, CreateNewSession if new_session else UseCurrentSession, api,
                                        password)
        await client.connect()
        await client.PrintSessions()
        await client.disconnect()
        return session_file

    except Exception as e:
        if os.path.exists(session_file):
            os.remove(session_file)


async def test_session(session_file):
    try:
        print(f"Testing session: {session_file}")

        client = TelegramClient(session_file)

        print("Connecting to Telegram...")
        await client.connect()

        if await client.is_user_authorized():
            print("Successfully authorized")

            me = await client.get_me()
            print(f"\nAccount Information:")
            print(f"  ID: {me.id}")
            print(f"  First Name: {me.first_name}")
            print(f"  Last Name: {me.last_name or 'None'}")
            print(f"  Username: @{me.username or 'None'}")
            print(f"  Phone: {me.phone or 'None'}")

            await client.get_me()
            print("Connection test passed")

        else:
            print("Not authorized")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()
        print("Disconnected")


async def main():
    session_file = await tdata_to_session_telethon("./tdata", "./")
    await test_session(session_file)


if __name__ == "__main__":
    asyncio.run(main())
