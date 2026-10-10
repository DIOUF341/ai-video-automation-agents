from typing import Any, Dict, List


class StoryboardScene:
    def __init__(
        self,
        scene_number: int,
        title: str,
        visual_prompt: str,
        duration_sec: int,
        camera: str = "plan large",
        text_overlay: str = "",
    ):
        self.scene_number = scene_number
        self.title = title
        self.visual_prompt = visual_prompt
        self.duration_sec = duration_sec
        self.camera = camera
        self.text_overlay = text_overlay


class StoryboardAgent:
    def build_storyboard(self, prompt: str, script: Dict[str, Any], style: str = "cinematic") -> Dict[str, Any]:
        scenes: List[StoryboardScene] = []
        for idx, scene in enumerate(script.get("scenes", []), start=1):
            visual_prompt = (
                f"{scene.get('title', f'Scène {idx}')} : {prompt} : style {style} : "
                "lumière élégante, composition moderne et visuel premium"
            )
            scenes.append(
                StoryboardScene(
                    scene_number=idx,
                    title=scene.get("title", f"Scène {idx}"),
                    visual_prompt=visual_prompt,
                    duration_sec=int(scene.get("duration", 5)),
                    camera=self._camera_for_scene(idx),
                    text_overlay=scene.get("title", f"Scène {idx}"),
                )
            )

        return {"scenes": scenes}

    @staticmethod
    def _camera_for_scene(index: int) -> str:
        cameras = [
            "plan large",
            "gros plan",
            "travelling latéral",
            "plan moyen",
            "plan rapproché",
            "plan final",
        ]
        return cameras[(index - 1) % len(cameras)]
