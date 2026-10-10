"""API FastAPI principale."""
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agents.script_agent import ScriptAgent
from agents.storyboard_agent import StoryboardAgent
from agents.voice_agent import VoiceAgent
from agents.video_renderer import VideoRenderer
from app.config import settings
from app.schemas import (
    ScriptGenerationRequest,
    ScriptGenerationResponse,
    VideoGenerationRequest,
    VideoGenerationResponse,
)

app = FastAPI(
    title=settings.app_name,
    description="Plateforme d'automatisation de création de vidéos assistée par IA",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "message": "Le générateur de script IA est prêt.",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "service": settings.app_name}


@app.post("/api/generate-script", response_model=ScriptGenerationResponse)
def generate_script(payload: ScriptGenerationRequest) -> ScriptGenerationResponse:
    try:
        agent = ScriptAgent(api_key=settings.openai_api_key, model=settings.openai_model)
        script = agent.generate(
            prompt=payload.prompt,
            duration=payload.duration,
            style=payload.style,
            language=payload.language,
        )
        return ScriptGenerationResponse(**script)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Erreur de parsing JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@app.post("/api/generate-video", response_model=VideoGenerationResponse)
def generate_video(payload: VideoGenerationRequest) -> VideoGenerationResponse:
    try:
        output_dir = Path(settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        script_agent = ScriptAgent(api_key=settings.openai_api_key, model=settings.openai_model)
        script = script_agent.generate(
            prompt=payload.prompt,
            duration=payload.duration,
            style=payload.style,
            language=payload.language,
        )

        storyboard_agent = StoryboardAgent()
        storyboard = storyboard_agent.build_storyboard(payload.prompt, script, style=payload.style)

        voice_agent = VoiceAgent()
        voice_path = voice_agent.generate_voice(
            text=script.get("voiceover", payload.prompt),
            output_name=payload.output_name,
            language=payload.language,
            output_dir=str(output_dir),
        )

        video_renderer = VideoRenderer(output_dir=str(output_dir))
        render_result = video_renderer.render(
            audio_path=voice_path,
            output_name=payload.output_name,
            duration=payload.duration,
            image_sequence=[],
        )

        return VideoGenerationResponse(
            title=script.get("title", "Vidéo IA"),
            summary=script.get("summary", payload.prompt),
            script_path=str(output_dir / f"{payload.output_name}_script.json"),
            voice_path=voice_path,
            video_path=render_result.get("output_path"),
            storyboard=storyboard.get("scenes", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(_, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc), "error_type": type(exc).__name__})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
