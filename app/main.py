from fastapi import FastAPI, HTTPException

from app.config import settings
from app.schemas import VideoRequest, VideoResponse
from workflows.video_pipeline import VideoPipeline

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="MVP d'IA pour automatiser la création de vidéos",
)

pipeline = VideoPipeline()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


@app.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest) -> VideoResponse:
    try:
        return pipeline.run(request)
    except Exception as exc:  # pragma: no cover - safe guard
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
