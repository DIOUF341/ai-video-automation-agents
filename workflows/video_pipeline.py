from agents.render_agent import RenderAgent
from agents.script_agent import ScriptAgent
from agents.storyboard_agent import StoryboardAgent
from agents.voice_agent import VoiceAgent
from app.schemas import VideoRequest, VideoResponse
from app.utils import ensure_output_dir, write_json


class VideoPipeline:
    def __init__(self):
        self.script_agent = ScriptAgent()
        self.storyboard_agent = StoryboardAgent()
        self.voice_agent = VoiceAgent()
        self.render_agent = RenderAgent()

    def run(self, request: VideoRequest) -> VideoResponse:
        script = self.script_agent.generate_script(request.prompt, request.duration)
        storyboard = self.storyboard_agent.build_storyboard(request.prompt, script, request.style)

        voice_file = self.voice_agent.generate_voice(script["full_text"], request.output_name, request.language)

        render_result = self.render_agent.render(
            request.prompt,
            script,
            storyboard,
            voice_file,
            request.output_name,
        )

        project_dir = ensure_output_dir() / request.output_name
        project_dir.mkdir(parents=True, exist_ok=True)

        manifest_payload = {
            "status": "success",
            "title": script["title"],
            "script_summary": script["full_text"][:200],
            "storyboard_scenes": [
                {
                    "scene_number": scene.scene_number,
                    "title": scene.title,
                    "visual_prompt": scene.visual_prompt,
                    "duration_sec": scene.duration_sec,
                }
                for scene in storyboard["scenes"]
            ],
            "output_dir": str(project_dir),
            "voice_file": voice_file,
            "video_file": render_result["video_file"],
            "manifest_file": render_result["manifest"],
        }

        manifest_path = project_dir / "final_manifest.json"
        manifest_path.write_text(str(manifest_payload), encoding="utf-8")

        return VideoResponse(
            status="success",
            title=script["title"],
            script_summary=script["full_text"][:200],
            storyboard_scenes=storyboard["scenes"],
            output_dir=str(project_dir),
            voice_file=voice_file,
            video_file=render_result["video_file"],
            manifest_file=str(render_result["manifest"]),
        )
