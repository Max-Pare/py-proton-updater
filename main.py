import requests, json, re, platform, random, os, time, tarfile, shutil, sys, subprocess
from pathlib import Path

GE_PROTON_REGEX = r'GE-Proton[0-9]{1,2}-[0-9]{1,2}\.tar\.gz$'
TMP_DIR = f'/tmp/py-proton-updater.{random.randint(1_000_000,9_999_999)}/'
PROTON_DIRS = {0: os.path.expanduser('~/.local/share/Steam/compatibilitytools.d/')} # I flatpak uses a different directory but I think it's symlinked to the same dir as native or something
STEAM_VER = 0
PROTON_REPO = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
HOME_DIR = os.path.expanduser('~')

def main():
    if os.geteuid() == 0: exit("Running this as root is a bad idea, quitting.")
    if not os.path.isdir(TMP_DIR): os.mkdir(TMP_DIR)
    global proton_dir
    proton_dir = PROTON_DIRS[STEAM_VER]
    download_file(get_latest_download_url())

def get_latest_download_url() -> str:
    assert os.path.isdir(proton_dir)
    _res = requests.get(PROTON_REPO)
    _res.raise_for_status()
    _res_json  = (json.loads(_res.content))
    try:
        return _res_json[0]['assets'][1]['browser_download_url'] # get newest item in releases 
    except Exception as e:
        die(e)

def download_file(download_url: str) -> str:
    print('Getting release page')
    file_name = Path(download_url).name
    proton_name_raw = Path(download_url).name.replace('.tar.gz','')
    print('Found ', proton_name_raw)
    print(f'Checking if "{proton_name_raw}" is already installed')
    if check_installed(proton_name_raw):
        print('You seem to already have the latest version of Proton-GE installed.')
        exit(0)
    print('Proton version not found, continuing with install.')
    file_download = requests.get(download_url)
    try:
        out_file = TMP_DIR + file_name
        print('Saving file to disk')
        with open(out_file, mode='wb') as file:
            file.write(file_download.content)
    except Exception as e1:
        die(e1)
    print('Extracting archive')
    with tarfile.open(out_file, mode='r:gz') as _tar:
        _tar.extractall(TMP_DIR)
    shutil.move(f'{TMP_DIR}/{proton_name_raw}', f'{proton_dir}/{proton_name_raw}')
    print(f'{proton_name_raw} successfully installed!')
    
def die(_ex: Exception):
    print(_ex.with_traceback())
    print("[FATAL]  Something happened: something happened")
    exit(-1)

def check_installed(_dir:str) -> bool:
    return os.path.isdir(f'{PROTON_DIRS[STEAM_VER]}/{_dir}')

def detect_cosmic_ray():
    print('Scanning for cosmic rays...')
    for _ in range(64):
        if True is False: raise ValueError('[FATAL] Cosmic ray detected, a full system reboot is reccomended, quitting.')
        time.sleep(0.003)
    print('No cosmic rays detected, starting...')

if __name__=='__main__':
    if platform.system == 'Windows': raise NotImplementedError('Windows is not supported.')
    if platform.system == 'Darwin': print('WARNING: Mac is not directly supported but it might still work.')
    detect_cosmic_ray()
    try:
        main()
    finally:
        os.remove(TMP_DIR)


# TODO:
# - download_file() function shouldn't do everything [50%]
# - refactor