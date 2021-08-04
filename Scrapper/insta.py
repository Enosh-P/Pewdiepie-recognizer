import re 
import shutil
import os
import json
import requests

from typing import Dict, List, Any
from bs4 import BeautifulSoup
from datetime import datetime

class Hashtag:

    def __init__(self, tag):
        self.tag_name = tag
        self.total_post = 0
        self.all_links = []
    
    @staticmethod
    def remove_unwanted(wid, hei, diff_img) -> List[str]:
        uni_links = []
        for img in diff_img:
            if img['width'] == wid and img['height'] == hei: uni_links += [img["url"]]
        return uni_links

    def authenticate(self) -> bool:
        time = int(datetime.now().timestamp())
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        header = {
                "User-Agent": "user-agent: Mozilla/5.0 (Linux)", 
                "cookie": f"sessionid={os.environ.get('sessionid')};"
                }
        payload = {
                'username': 'peterponrajenosh@gmail.com',
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:Hanna@10051996'
                }
        self.session = requests.Session()
        response = self.session.get(link, headers = header)
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",response.text)[0]
        response = self.session.post(login_url,data=payload,headers={
            "user-agent": "Mozilla/5.0 (Linux)",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken":csrf
            })
        if response.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def to_json(source) -> Dict:
        ht_soup = BeautifulSoup(source, features="html.parser")
        jd = []
        js = [str(script) for script in ht_soup.find_all("script") if "config" in str(script)]
        for st in js:
            left_index = st.find("{")
            right_index = st.rfind("}") + 1
            json_str = st[left_index:right_index]
            jd.append(json_str)
        nw_jd = [json.loads(j_str) for j_str in jd]
        if len(nw_jd) == 1:
            j_dict = nw_jd[0]
        else:
            j_dict = nw_jd[1]
        return j_dict

    def get_links(self):
        if not self.authenticate():
            raise ValueError("Athentication Failed. Check the credentials")
        ht_link = f'https://www.instagram.com/explore/tags/{self.tag_name}/'
        self.ht_source = self.session.get(ht_link).text
        self.json_dict = self.to_json(self.ht_source)
        top = self.json_dict['entry_data']["TagPage"][0]['data']['top']['sections']
        recent = self.json_dict['entry_data']["TagPage"][0]['data']['recent']['sections']
        for i in range(len(top)):
            media = top[i]['layout_content']['medias']
            for j in range(len(media)):
                if not media[j]['media'].get('original_width') or not media[j]['media'].get('original_height'):
                    continue
                else:
                    oh = media[j]['media']['original_height']
                    ow = media[j]['media']['original_width']
                self.all_links += self.remove_unwanted(ow, oh, media[j]['media']['image_versions2']['candidates'])
        for i in range(len(recent)):
            media_2 = recent[i]['layout_content']['medias']
            for j in range(len(media_2)):
                if not media_2[j]['media'].get('original_width') or not media_2[j]['media'].get('original_height'):
                    continue
                else:
                    oh = media_2[j]['media']['original_height']
                    ow = media_2[j]['media']['original_width']
                self.all_links += self.remove_unwanted(ow, oh, media_2[j]['media']['image_versions2']['candidates'])
        self.total_post = len(self.all_links)

    def download_images(self, destination) -> None:
        os.system(f"mkdir -p {destination}")
        for i, image_url in enumerate(self.all_links):
            res = requests.get(image_url, stream = True)
            if res.status_code == 200:
                res.raw.decode_content = True
                with open(f'{destination}/test_image{str(i)}.jpg','wb') as f:
                    shutil.copyfileobj(res.raw, f)
