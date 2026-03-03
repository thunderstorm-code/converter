'''
Если будете использовать / пастить где либо данный конвертер то упомяните меня
если не жаль конечно <3 [@buyclown / @suckdollar]
сам код конвертера начинается с 108 строчки что бы вам не искать
'''
import os
import sys
import asyncio
import tempfile
import zipfile
import shutil
import time
from colorama import init, Fore, Style
import tkinter as tk
from tkinter import filedialog
init()


def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def _pick_file(title, types_):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    p = filedialog.askopenfilename(title=title, filetypes=types_)
    root.destroy()
    return p

def _pick_dir(title):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    p = filedialog.askdirectory(title=title)
    root.destroy()
    return p

def _red(s):
    return Fore.RED + s + Style.RESET_ALL


def _green(s):
    return Fore.GREEN + s + Style.RESET_ALL

def _load_module_from_path(module_name, file_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(module_name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _resolve_converters():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        import t_to_s as _t_to_s
    except Exception:
        _t_to_s = _load_module_from_path('t_to_s', os.path.join(base_dir, 't_to_s.py'))
    try:
        import s_to_y as _s_to_y
    except Exception:
        _s_to_y = _load_module_from_path('s_to_y', os.path.join(base_dir, 's_to_y.py'))
    tdata_to_session_telethon = _t_to_s.tdata_to_session_telethon
    test_session = getattr(_t_to_s, 'test_session', None)
    session_to_tdata = _s_to_y.session_to_tdata
    return tdata_to_session_telethon, test_session, session_to_tdata

def _extract_zip(zip_path):
    temp_dir = tempfile.mkdtemp(prefix='tdata_zip_')
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(temp_dir)
    return temp_dir

def _find_tdata_folder(root_dir):
    root_dir = os.path.abspath(root_dir)
    direct = os.path.join(root_dir, 'tdata')
    if os.path.isdir(direct):
        return direct

    def looks_like_tdata_dir(p):
        if not os.path.isdir(p):
            return False
        try:
            names = set(os.listdir(p))
        except Exception:
            return False
        if 'key_datas' in names or 'map0' in names:
            return True
        for n in names:
            if n.startswith('D') and len(n) >= 10:
                return True
        return False

    if looks_like_tdata_dir(root_dir):
        return root_dir

    for cur, dirs, files in os.walk(root_dir):
        if 'tdata' in dirs:
            return os.path.join(cur, 'tdata')

    for cur, dirs, files in os.walk(root_dir):
        if looks_like_tdata_dir(cur):
            return cur

    raise FileNotFoundError('tdata not found in zip')

######НАЧАЛО ФУНКЦИЙ КОНВЕРТАЦИИ###
async def tdata_zip_to_session(zip_path, out_dir):
    tdata_to_session_telethon, test_session, _ = _resolve_converters()
    temp_dir = None
    ok = False
    try:
        temp_dir = _extract_zip(zip_path)
        tdata_dir = _find_tdata_folder(temp_dir)
        session_file = await tdata_to_session_telethon(tdata_dir, out_dir)
        if not session_file:
            raise RuntimeError('empty session path')
        ok = True
    except Exception as e:
        print(f'Error: {e}')
        ok = False
    finally:
        if temp_dir and os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    return ok

async def session_to_tdata_with_test(session_path, out_dir):
    tdata_to_session_telethon, test_session, session_to_tdata = _resolve_converters()
    work = tempfile.mkdtemp(prefix='s2t_work_')
    cwd = os.getcwd()
    ok = False
    try:
        os.chdir(work)
        await session_to_tdata(session_path)
        src_root = os.path.join(work, 'from_session_to_tdata', 'tdatas')
        if not os.path.isdir(src_root):
            raise RuntimeError('output folder not found')
        os.makedirs(out_dir, exist_ok=True)
        for name in os.listdir(src_root):
            src = os.path.join(src_root, name)
            dst = os.path.join(out_dir, name)
            if os.path.exists(dst):
                shutil.rmtree(dst, ignore_errors=True)
            shutil.move(src, dst)
        ok = True
    except Exception as e:
        print(f'Error: {e}')
        ok = False
    finally:
        os.chdir(cwd)
        shutil.rmtree(work, ignore_errors=True)
    return ok
######КОНЕЦ ФУНКЦИЙ КОНВЕРТАЦИИ###

def _hold_open():
    while True:
        time.sleep(3600)

def main():
    print(f"Hello, this program is fully open-source and includes its source code.\nDuring conversion, your sessions and other data are not sent to {_red('anyone')}.\nI’ll be glad if this program is useful to you! For errors or questions, please write to > @buyclowm <3")
    print("1. session -> tdata")
    print("2. tdata -> session")
    choice = input("> ").strip()

    if choice == '1':
        sp = _pick_file('Выбери .session', [('Telethon session', '*.session'), ('All files', '*.*')])
        if not sp:
            _hold_open()
        out_dir = _pick_dir('Куда сохранить tdata?')
        if not out_dir:
            _hold_open()
        _clear()
        print("wait")
        time.sleep(0.05)
        _clear()
        ok = asyncio.run(session_to_tdata_with_test(sp, out_dir))
        if ok:
            print(_green("Result - DONE"))
        else:
            print(_red("Result - FAILED"))
        _hold_open()

    if choice == '2':
        zp = _pick_file('Выбери ZIP', [('ZIP files', '*.zip')])
        if not zp:
            _hold_open()
        out_dir = _pick_dir('Куда сохранить .session?')
        if not out_dir:
            _hold_open()
        _clear()
        print("wait")
        time.sleep(0.05)
        _clear()
        ok = asyncio.run(tdata_zip_to_session(zp, out_dir))
        if ok:
            print(_green("Result - DONE"))
        else:
            print(_red("Result - FAILED"))
        _hold_open()

    _hold_open()

if __name__ == '__main__':
    main()
