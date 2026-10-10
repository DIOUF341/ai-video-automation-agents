from typing import Dict, List


class ScriptAgent:
    def generate_script(self, prompt: str, duration: int) -> Dict:
        prompt_clean = (prompt or "Vidéo d'entreprise").strip()
        base_title = prompt_clean[:60].strip()
        if not base_title:
            base_title = "Vidéo automatisée"

        scene_text = [
            f"Introduction : {prompt_clean}",
            "Le contexte et le problème à résoudre.",
            "La solution, la valeur ajoutée et les bénéfices.",
            "Exemple de mise en œuvre rapide.",
            "Conclusion et appel à l'action.",
        ]

        scenes = []
        for index, sentence in enumerate(scene_text, start=1):
            scenes.append(
                {
                    "title": f"Scène {index}",
                    "text": sentence,
                    "duration_sec": max(4, int(duration / len(scene_text))),
                }
            )

        full_text = " ".join(scene["text"] for scene in scenes)

        return {
            "title": base_title,
            "full_text": full_text,
            "scenes": scenes,
        }
