import requests
import json
import re
file_pattern = r'GE-Proton[0-9]{1,2}-[0-9]{1,2}\.tar\.gz$'

def download_file():
    req = requests.get("https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases")
    req.raise_for_status()
    jreq  = (json.loads(req.content))
    try:
        d_url = jreq[0].get('assets')[1].get('browser_download_url') # get newest item in releases 
        # print(d_url)
    except Exception as e:
        print(e.with_traceback())
        print("[FATAL] Something happened: something happened")
    file_name = re.search(file_pattern, d_url).group()
    data = requests.get(d_url)
    with open('./'+file_name, mode='wb') as file:
        file.write(data.content)

if __name__=='__main__':
    download_file()        

    
            


