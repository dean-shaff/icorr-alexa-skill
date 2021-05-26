from urllib.parse import urljoin
import os

import requests
from PIL import Image
from bs4 import BeautifulSoup


TMP_DIR = os.environ.get("TMP_DIR", ".")


def get_color(img):
    return img.getpixel((295, 60))



def app():

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
            img_path = os.path.join(TMP_DIR, "_image.png")
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
    app()
