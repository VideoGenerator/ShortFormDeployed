from flask import Flask, jsonify
from flask_cors import CORS
from tiktok_maker import fetch_and_download_twitch_clip
from mashup import process_videos

flaskapp = Flask(__name__)
CORS(flaskapp)


@flaskapp.route("/get_twitch_clip/<username>", methods=["GET"])
def get_twitch_clip(username):
    fetch_and_download_twitch_clip(username)
    video_name, public_url = process_videos()

    return jsonify(
        {
            "video_name": video_name,
            "public_url": public_url,
        }
    )


if __name__ == "__main__":
    flaskapp.run(debug=True)