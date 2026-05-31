# process video
import os
import shutil
import subprocess
import tempfile

import easyocr
import gdown

reader = easyocr.Reader(['en'])


def generate_ocr_from_video(video_link):

    temp_dir = tempfile.mkdtemp()

    try:

        video_path = os.path.join(
            temp_dir,
            "video.mp4"
        )

        gdown.download(
            video_link,
            video_path,
            quiet=False,
            fuzzy=True
        )

        frames_dir = os.path.join(
            temp_dir,
            "frames"
        )

        os.makedirs(frames_dir)

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-vf",
                "fps=1",
                f"{frames_dir}/frame_%04d.jpg",
                "-y"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        all_text = []

        for frame in sorted(
            os.listdir(frames_dir)
        ):

            frame_path = os.path.join(
                frames_dir,
                frame
            )

            try:

                results = reader.readtext(
                    frame_path
                )

                for result in results:

                    text = result[1].strip()

                    if len(text) > 2:
                        all_text.append(text)

            except Exception:
                pass

        unique_text = list(
            dict.fromkeys(all_text)
        )

        return " ".join(unique_text)

    finally:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )
