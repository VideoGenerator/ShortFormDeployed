import requests
import os
import shutil


def clear_clips_folder():
    folder = "clips"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def download_clip(thumbnail_url):
    clear_clips_folder()
    index = thumbnail_url.find("-preview")
    clip_url = thumbnail_url[:index] + ".mp4"

    r = requests.get(clip_url)

    if (
        "Content-Type" in r.headers
        and r.headers["Content-Type"] == "binary/octet-stream"
    ):
        filename = thumbnail_url.split("/")[-1].replace("-preview", "") + ".mp4"
        with open(os.path.join("clips", filename), "wb") as f:
            f.write(r.content)

    else:
        print(f"Failed to download clip from thumb: {thumbnail_url}")