from urllib.parse import urljoin
import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
bundle_dir = os.path.join(cur_dir, "bundle")

tmp_dir = "."
ENV = os.environ.get("ENV", "development")
if ENV == "production":
    sys.path.append(bundle_dir)
    tmp_dir = "/tmp"


import requests # noqa E402
from PIL import Image # noqa E402
from bs4 import BeautifulSoup # noqa E402


def get_color(img):
    return img.getpixel((295, 60))


def handler():

    url = "http://www.icorrmtb.org/mobile/"

    with requests.Session() as session:
        res = session.get(url)
        soup = BeautifulSoup(res.text, features="lxml")
        img_url = None
        for img in soup.find_all("img"):
            if "trail status" in img.get("alt").lower():
                link = img.get("src")
                img_url = urljoin(url, link)
                break
        if img_url is not None:
            res = session.get(img_url, stream=True)
            img_path = os.path.join(tmp_dir, "_image.png")
            with open(img_path, "wb") as fd:
                for chunk in res:
                    fd.write(chunk)
            img = Image.open(img_path)
            color = get_color(img)
            if color == (179, 29, 35, 255):
                print("trails are closed!")
            else:
                print("trails are open!")
            os.remove(img_path)

        else:
            raise RuntimeError("Couldn't find image link!")


if __name__ == "__main__":
    handler()
