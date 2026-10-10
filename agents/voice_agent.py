from pathlib import Path

try:
    from gtts import gTTS
except Exception:  # pragma: no cover - library may not be installed in some envs
    gTTS = None

from app.config import settings


class VoiceAgent:
    def generate_voice(self, text: str, output_name: str, language: str = "fr") -> str:
        output_dir = Path(settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        voice_path = output_dir / f"{output_name}.mp3"

        if gTTS is not None:
            tts = gTTS(text=text, lang=language)
            tts.save(str(voice_path))
            return str(voice_path)

        fallback_path = output_dir / f"{output_name}.txt"
        fallback_path.write_text(text, encoding="utf-8")
        return str(fallback_path)
