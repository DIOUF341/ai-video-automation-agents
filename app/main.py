"""API FastAPI principale."""
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import ScriptGenerationRequest, ScriptGenerationResponse
from agents.script_agent import ScriptAgent

app = FastAPI(
    title=settings.app_name,
    description="Plateforme d'automatisation de création de vidéos assistée par IA",
    version="0.1.0",
)

# Activer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict:
    """Endpoint racine."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "message": "Le générateur de script IA est prêt.",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check() -> dict:
    """Vérifier l'état du service."""
    return {
        "status": "healthy",
        "service": settings.app_name,
    }


@app.post("/api/generate-script", response_model=ScriptGenerationResponse)
def generate_script(payload: ScriptGenerationRequest) -> ScriptGenerationResponse:
    """Générer un script vidéo à partir d'un prompt.
    
    Args:
        payload: Requête de génération contenant prompt, durée, style, langue
        
    Returns:
        Script structuré avec scènes et narration
        
    Raises:
        HTTPException: En cas d'erreur lors de la génération
    """
    try:
        agent = ScriptAgent(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )
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


@app.exception_handler(Exception)
async def global_exception_handler(_, exc: Exception):
    """Gestionnaire global d'exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "error_type": type(exc).__name__},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
