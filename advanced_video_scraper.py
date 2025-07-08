import requests
from bs4 import BeautifulSoup
import yt_dlp
import re
import sys
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_video_link_from_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Try finding common video iframe or embed link
        iframe_tags = soup.find_all("iframe")
        for tag in iframe_tags:
            src = tag.get("src", "")
            if "vidstream" in src or "player" in src or "embed" in src:
                return src

        # Try extracting m3u8 or mp4 links
        m3u8_links = re.findall(r'https?://[^\s"]+\.m3u8', response.text)
        if m3u8_links:
            return m3u8_links[0]

        mp4_links = re.findall(r'https?://[^\s"]+\.mp4', response.text)
        if mp4_links:
            return mp4_links[0]

        print("⚠️ لم يتم العثور على رابط مباشر للفيديو.")
        return None
    except Exception as e:
        print(f"❌ خطأ أثناء تحليل الصفحة: {e}")
        return None

def download_video(video_url):
    try:
        print(f"⬇️ تحميل الفيديو من: {video_url}")
        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "format": "best",
            "quiet": False
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("✅ تم تحميل الفيديو بنجاح.")
    except Exception as e:
        print(f"❌ فشل في التحميل: {e}")

def main():
    if len(sys.argv) != 2:
        print("🔰 الاستعمال: python script.py <رابط_الصفحة>")
        return
    page_url = sys.argv[1]
    print("🔍 استخراج الرابط من الصفحة...")
    video_link = get_video_link_from_page(page_url)
    if video_link:
        download_video(video_link)

if __name__ == "__main__":
    main()
