#!/usr/bin/env python3

import json, os, requests

current_dir = os.path.dirname(os.path.realpath(__file__))
base_url = "https://arc.msn.com/v3/Delivery/Placement?pid=209567&fmt=json&rafb=0&ua=WindowsShellClient%2F0&cdm=1&disphorzres=9999&dispvertres=9999&lo=80217&pl=en-US&lc=en-US&ctry=us"
target_image = None

def get_image_link():
    ua = "Mozilla/5.0"
    headers = { "User-Agent" : ua }
    data = requests.get(base_url, headers=headers)
    jobj = json.loads(data.content.decode("utf-8"))
    item = json.loads(jobj["batchrsp"]["items"][0]["item"])
    return item["ad"]["image_fullscreen_001_landscape"]['u']

def download_image(img_link):
    if img_link is not None:
        img = requests.get(img_link)
        img_file = open(os.path.join(current_dir, "spotlight", "slick-greeter.jpg"), "wb")
        img_file.write(img.content)
        img_file.close()
        return img_file.name
    return None

def set_lockscreen_background():
    path = download_image(get_image_link())
    path = '\/'.join(path.split('/'))
    os.system("sed -i -r 's/^background=.*/background={0}/' /etc/lightdm/slick-greeter.conf".format(path))

set_lockscreen_background()
