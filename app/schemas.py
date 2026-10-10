from typing import List, Optional

from pydantic import BaseModel, Field


class ScriptScene(BaseModel):
    title: str
    text: str
    duration_sec: int


class StoryboardScene(BaseModel):
    scene_number: int
    title: str
    visual_prompt: str
    duration_sec: int


class VideoRequest(BaseModel):
    prompt: str = Field(..., min_length=5, description="Idée de la vidéo")
    duration: int = Field(default=30, ge=10, le=180)
    style: str = Field(default="cinematic", description="Style visuel")
    language: str = Field(default="fr")
    voice: str = Field(default="fr")
    output_name: str = Field(default="video_generation")


class VideoResponse(BaseModel):
    status: str
    title: str
    script_summary: str
    storyboard_scenes: List[StoryboardScene]
    output_dir: str
    voice_file: Optional[str] = None
    video_file: Optional[str] = None
    manifest_file: str
