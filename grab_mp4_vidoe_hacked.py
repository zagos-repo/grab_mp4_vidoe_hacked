import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

def extract_mp4_url(page_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(page_url, headers=headers)

    if response.status_code != 200:
        print(" Page failed to load :).")
        return None

    soup = BeautifulSoup(response.text, "html.parser")


    for tag in soup.find_all(["video", "source"]):
        src = tag.get("src")
        if src and ".mp4" in src:
            return urljoin(page_url, src)


    mp4s = re.findall(r'src=["\'](.*?\.mp4.*?)["\']', response.text)
    if mp4s:
        return urljoin(page_url, mp4s[0])

    print(" We did not find a link mp4.")
    return None

def download_mp4(url, filename="video.mp4"):
    print(f" Download video from: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                f.write(chunk)
        print(f" Saved for ...: {filename}")
    else:
        print(" Page failed to load.")

if __name__ == "__main__":
    link = input(" Enter the page link: ").strip()
    mp4_url = extract_mp4_url(link)
    if mp4_url:
        file_name = os.path.basename(mp4_url.split("?")[0])
        download_mp4(mp4_url, file_name)
