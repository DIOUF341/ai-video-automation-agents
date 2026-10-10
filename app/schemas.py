"""Schémas Pydantic pour les requêtes et réponses."""
from pydantic import BaseModel, Field


class SceneSchema(BaseModel):
    """Schéma d'une scène vidéo."""
    title: str = Field(..., description="Titre de la scène")
    visual: str = Field(..., description="Description visuelle")
    narration: str = Field(..., description="Narration / dialogue")
    duration: int = Field(..., ge=1, description="Durée en secondes")


class ScriptGenerationRequest(BaseModel):
    """Requête de génération de script."""
    prompt: str = Field(..., min_length=10, description="Sujet de la vidéo")
    duration: int = Field(default=30, ge=10, le=180, description="Durée en secondes")
    style: str = Field(
        default="cinematic",
        description="Style visuel (cinematic, social, corporate)"
    )
    language: str = Field(default="fr", description="Langue de la voix off")
    voice: str = Field(default="fr", description="Voix ou profil vocal")


class ScriptGenerationResponse(BaseModel):
    """Réponse de génération de script."""
    title: str = Field(..., description="Titre de la vidéo")
    summary: str = Field(..., description="Résumé du script")
    duration_seconds: int = Field(..., description="Durée totale en secondes")
    style: str = Field(..., description="Style visuel")
    language: str = Field(..., description="Langue")
    scenes: list[SceneSchema] = Field(..., description="Liste des scènes")
    voiceover: str = Field(..., description="Narration générale")
