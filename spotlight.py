#!/usr/bin/env python3

import json, os, requests

current_dir = os.path.dirname(os.path.realpath(__file__))
base_url = "https://arc.msn.com/v3/Delivery/Cache?pid=209567&fmt=json&lc=en-US&ctry=SG"
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
