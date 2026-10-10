from typing import Dict, List

from app.schemas import StoryboardScene


class StoryboardAgent:
    def build_storyboard(self, prompt: str, script: Dict, style: str = "cinematic") -> Dict:
        scenes: List[StoryboardScene] = []
        for idx, scene in enumerate(script["scenes"], start=1):
            visual_prompt = (
                f"{scene['title']} : {prompt} : style {style} : lumière élégante et visuel moderne"
            )
            scenes.append(
                StoryboardScene(
                    scene_number=idx,
                    title=scene["title"],
                    visual_prompt=visual_prompt,
                    duration_sec=scene["duration_sec"],
                )
            )

        return {"scenes": scenes}
