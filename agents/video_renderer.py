import subprocess
from pathlib import Path
from typing import List, Optional


class VideoRenderer:
    """Rend un MP4 final à partir d'un fichier audio et d'une liste d'images."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render(
        self,
        audio_path: str,
        output_name: str = "final_video",
        duration: int = 30,
        image_sequence: Optional[List[str]] = None,
    ) -> dict:
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Le fichier audio est introuvable : {audio_path}")

        final_name = self._sanitize_name(output_name)
        output_mp4 = self.output_dir / f"{final_name}.mp4"

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=1280x720:d=1",
            "-i",
            audio_path,
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-shortest",
            str(output_mp4),
        ]

        if image_sequence:
            temp_dir = self.output_dir / "tmp_frames"
            temp_dir.mkdir(exist_ok=True)
            for idx, img in enumerate(image_sequence[:10], start=1):
                src = Path(img)
                if src.exists():
                    subprocess.run(["cp", str(src), str(temp_dir / f"frame_{idx:03d}.png")], check=False)
            if any((temp_dir / f"frame_{i:03d}.png").exists() for i in range(1, 11)):
                frame_pattern = str(temp_dir / "frame_%03d.png")
                command = [
                    "ffmpeg",
                    "-y",
                    "-framerate",
                    "1",
                    "-i",
                    frame_pattern,
                    "-i",
                    audio_path,
                    "-c:v",
                    "libx264",
                    "-preset",
                    "fast",
                    "-crf",
                    "23",
                    "-c:a",
                    "aac",
                    "-shortest",
                    str(output_mp4),
                ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except FileNotFoundError as exc:
            raise RuntimeError("FFmpeg n'est pas installé ou n'est pas disponible dans le PATH.") from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"FFmpeg a échoué : {exc.stderr or exc.stdout or 'Erreur inconnue'}") from exc

        return {
            "output_path": str(output_mp4),
            "file_name": f"{final_name}.mp4",
            "duration": duration,
            "size_bytes": output_mp4.stat().st_size,
        }

    @staticmethod
    def _sanitize_name(value: str) -> str:
        safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value.strip().lower())
        return safe or "final_video"
