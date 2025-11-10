import requests
import json
import re
import platform
import random
import os
import time
from pathlib import Path
import tarfile
import shutil

GE_PROTON_REGEX = r'GE-Proton[0-9]{1,2}-[0-9]{1,2}\.tar\.gz$'
TMP_DIR = f'/tmp/py-proton-updater.{random.randint(1_000_000,9_999_999)}/'
PROTON_DIRS = {0: os.path.expanduser('~/.local/share/Steam/compatibilitytools.d/')} # I flatpak uses a different directory but I think it's symlinked to the same dir as native or something
STEAM_VER = 0
PROTON_REPO = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
HOME_DIR = os.path.expanduser('~')

def main():
    if os.geteuid() == 0: exit("Do not run this script as root because...BECAUSE YOU CAN'T OKAY???")
    if not os.path.isdir(TMP_DIR): os.mkdir(TMP_DIR)
    download_file()


def download_file() -> str: # this does too much
    print('Getting Proton-GE release page...')
    proton_dir = PROTON_DIRS[STEAM_VER]
    print(proton_dir)
    assert os.path.isdir(proton_dir)
    _res = requests.get(PROTON_REPO)
    _res.raise_for_status()
    print('Done')
    _res_json  = (json.loads(_res.content))
    try:
        print('Getting latest Proton-GE version...')
        d_url = _res_json[0].get('assets')[1].get('browser_download_url') # get newest item in releases 
    except Exception as e:
        die(e)
    
    file_name = Path(d_url).name
    proton_name_raw = Path(d_url).name.replace('.tar.gz','')
    if check_latest_installed(proton_name_raw):
        print('You seem to already have the latest Proton-GE version.')
        exit(0)

    print('Done\nDownloading...')
    file_download = requests.get(d_url)
    try:
        out_file = TMP_DIR + file_name
        with open(out_file, mode='wb') as file:
            file.write(file_download.content)
            print('File downloaded.') 
    except Exception as e1:
        die(e1)
    print('Extracting archive to steam directory...')
    with tarfile.open(out_file, mode='r:gz') as _tar:
        _tar.extractall(TMP_DIR)
    shutil.move(f'{TMP_DIR}/{proton_name_raw}', f'{proton_dir}/{proton_name_raw}')
    print(f'{proton_name_raw} successfully installed!')
    
def die(_ex: Exception):
    print(_ex.with_traceback())
    print("[FATAL]  Something happened: something happened")
    exit(-1)

def check_latest_installed(_latest: str) -> bool:
    return os.path.isdir(f'{PROTON_DIRS[STEAM_VER]}/{_latest}')

def detect_cosmic_ray():
    print('Scanning for cosmic rays...')
    for _ in range(64):
        if True is False: raise ValueError('[FATAL]  Cosmic ray detected, quitting...')
        time.sleep(0.003)
    print('No cosmic rays detected, launching program.')

if __name__=='__main__':
    if platform.system == 'Windows': raise NotImplementedError('Windows is not supported.')
    if platform.system == 'Darwin': print('WARNING: Mac is not directly supported but it might still work.')
    detect_cosmic_ray()
    main()


# TODO:
# - download_file() function shouldn't do everything 
# - refactor