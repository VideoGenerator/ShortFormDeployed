import firebase_admin
from firebase_admin import credentials, storage
from moviepy.editor import VideoFileClip, CompositeVideoClip
from io import BytesIO
import random
import os
import tempfile

# Initialize Firebase Admin
firebaseKey = "../serviceAccountKey.json"
cred = credentials.Certificate(firebaseKey)
firebase_admin.initialize_app(cred, {"storageBucket": "brainrot-24a7a.appspot.com"})


def process_videos():
    # Find the first video file in the clips folder
    clips_folder = "clips"
    video_files = [f for f in os.listdir(clips_folder) if f.endswith(".mp4")]
    # Split the filename to remove the first extension
    video1_name, _ = os.path.splitext(video_files[0])

    # Split again to remove the second extension if it exists
    video1_name, _ = os.path.splitext(video1_name)

    if not video_files:
        # print("No video files found in the clips folder.")
        return
    video1_path = os.path.join(clips_folder, video_files[0])
    video2_path = "minecraft/minecraftvideo.mp4"

    # Load the videos
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)

    # Determine the shorter duration
    random_number = random.randint(0, 250)
    end_clip = random_number + min(clip1.duration, clip2.duration)

    # Trim both videos to the shorter duration
    clip1_trimmed = clip1
    clip2_trimmed = clip2.subclip(random_number, end_clip)

    # Determine the minimum width (for consistent width)
    min_width = min(clip1_trimmed.size[0], clip2_trimmed.size[0])

    # Resize (downscale only) the videos and keep the width consistent
    clip1_resized = clip1_trimmed.resize(width=min_width)
    clip2_resized = clip2_trimmed.resize(width=min_width)

    # Calculate heights for 1/4 and 3/4 split
    total_height = clip1_resized.size[1] + clip2_resized.size[1]
    clip1_height = total_height // 3
    clip2_height = total_height - clip1_height

    # Resize clips to their respective heights
    clip1_final = clip1_resized.resize(height=clip1_height)
    clip2_final = clip2_resized.resize(height=clip2_height)

    # Stack the videos with the specified size ratio
    final_clip = CompositeVideoClip(
        [
            clip1_final.set_position(("center", "top")),
            clip2_final.set_position(("center", "bottom")),
        ],
        size=(min_width, clip1_height + clip2_height),
    )

    # Set the audio of the first video to the final clip
    final_clip = final_clip.set_audio(clip1_trimmed.audio)

    # Ensure the final video has a 9:16 aspect ratio
    target_aspect_ratio = 9 / 16
    target_height = final_clip.size[1]
    target_width = int(target_height * target_aspect_ratio)

    # Crop around the center to achieve 9:16 aspect ratio
    final_clip_cropped = final_clip.crop(
        width=target_width,
        height=target_height,
        x_center=final_clip.size[0] / 2,
        y_center=final_clip.size[1] / 2,
    )

    # Write to a temporary file and read it into a BytesIO object
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        final_clip_cropped.write_videofile(
            temp_file.name,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            ffmpeg_params=["-crf", "26"],
            threads="auto",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )
        temp_file_path = temp_file.name

    final_buffer = BytesIO()
    with open(temp_file_path, "rb") as temp_file:
        final_buffer.write(temp_file.read())
    final_buffer.seek(0)

    # Upload to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(f"{video1_name}.mp4")
    blob.upload_from_file(final_buffer, content_type="video/mp4")
    blob.make_public()
    print(blob.public_url)

    # Close the buffer and delete the temporary file
    final_buffer.close()
    os.remove(temp_file_path)
    return video1_name, blob.public_url