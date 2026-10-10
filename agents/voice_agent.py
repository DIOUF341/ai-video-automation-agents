from pathlib import Path

try:
    from gtts import gTTS
except Exception:  # pragma: no cover
    gTTS = None


class VoiceAgent:
    def generate_voice(self, text: str, output_name: str, language: str = "fr", output_dir: str = "output") -> str:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        voice_path = output_path / f"{output_name}.mp3"

        if gTTS is not None:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(voice_path))
            return str(voice_path)

        fallback = output_path / f"{output_name}.txt"
        fallback.write_text(text, encoding="utf-8")
        return str(fallback)
