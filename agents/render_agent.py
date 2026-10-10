import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from app.config import settings


class RenderAgent:
    def render(self, prompt: str, script: dict, storyboard: dict, voice_file: str, output_name: str) -> dict:
        output_dir = Path(settings.output_dir)
        project_dir = output_dir / output_name
        project_dir.mkdir(parents=True, exist_ok=True)

        poster_path = project_dir / "poster.png"
        self._create_poster(script["title"], prompt, poster_path)

        manifest = {
            "title": script["title"],
            "prompt": prompt,
            "storyboard": [
                {
                    "scene_number": scene.scene_number,
                    "title": scene.title,
                    "visual_prompt": scene.visual_prompt,
                    "duration_sec": scene.duration_sec,
                }
                for scene in storyboard["scenes"]
            ],
            "voice_file": voice_file,
            "poster": str(poster_path),
        }

        manifest_path = project_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        video_path = None
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg and voice_file.endswith(".mp3"):
            video_path = project_dir / "video.mp4"
            command = [
                ffmpeg,
                "-y",
                "-loop",
                "1",
                "-t",
                "10",
                "-i",
                str(poster_path),
                "-i",
                str(voice_file),
                "-shortest",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-movflags",
                "+faststart",
                str(video_path),
            ]
            import subprocess

            subprocess.run(command, check=False)

        return {
            "project_dir": str(project_dir),
            "poster": str(poster_path),
            "manifest": str(manifest_path),
            "video_file": str(video_path) if video_path else None,
        }

    def _create_poster(self, title: str, prompt: str, output_path: Path) -> None:
        width, height = 1280, 720
        image = Image.new("RGB", (width, height), color=(16, 24, 40))
        draw = ImageDraw.Draw(image)

        start_x = 80
        start_y = 110
        draw.rectangle((60, 60, width - 60, height - 60), outline=(120, 180, 255), width=4)
        draw.text((start_x, start_y), title[:35], fill=(255, 255, 255), anchor=None)
        draw.text((start_x, start_y + 120), prompt[:80], fill=(170, 210, 255), anchor=None)
        draw.text((start_x, height - 140), "VideoAgent Studio", fill=(200, 220, 255), anchor=None)

        image.save(output_path, format="PNG")
