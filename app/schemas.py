"""Schémas Pydantic pour les requêtes et réponses."""
from pydantic import BaseModel, Field


class SceneSchema(BaseModel):
    title: str = Field(..., description="Titre de la scène")
    visual: str = Field(..., description="Description visuelle")
    narration: str = Field(..., description="Narration / dialogue")
    duration: int = Field(..., ge=1, description="Durée en secondes")


class ScriptGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Sujet de la vidéo")
    duration: int = Field(default=30, ge=10, le=180, description="Durée en secondes")
    style: str = Field(default="cinematic", description="Style visuel (cinematic, social, corporate)")
    language: str = Field(default="fr", description="Langue de la voix off")
    voice: str = Field(default="fr", description="Voix ou profil vocal")


class ScriptGenerationResponse(BaseModel):
    title: str = Field(..., description="Titre de la vidéo")
    summary: str = Field(..., description="Résumé du script")
    duration_seconds: int = Field(..., description="Durée totale en secondes")
    style: str = Field(..., description="Style visuel")
    language: str = Field(..., description="Langue")
    scenes: list[SceneSchema] = Field(..., description="Liste des scènes")
    voiceover: str = Field(..., description="Narration générale")


class StoryboardSceneSchema(BaseModel):
    scene_number: int = Field(..., description="Numéro de scène")
    title: str = Field(..., description="Titre de la scène")
    visual_prompt: str = Field(..., description="Prompt visuel pour générer l'image")
    duration_sec: int = Field(..., description="Durée de la scène en secondes")
    camera: str = Field(..., description="Type de plan de caméra")
    text_overlay: str = Field(..., description="Texte à afficher sur l'image")


class StoryboardGenerationResponse(BaseModel):
    scenes: list[StoryboardSceneSchema] = Field(..., description="Storyboard complet")


class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Sujet de la vidéo")
    duration: int = Field(default=30, ge=10, le=180, description="Durée en secondes")
    style: str = Field(default="cinematic", description="Style visuel")
    language: str = Field(default="fr", description="Langue de la voix off")
    output_name: str = Field(default="video_output", description="Nom du fichier exporté")


class VideoGenerationResponse(BaseModel):
    title: str = Field(..., description="Titre de la vidéo")
    summary: str = Field(..., description="Résumé")
    script_path: str | None = Field(default=None, description="Chemin du script généré")
    voice_path: str | None = Field(default=None, description="Chemin du fichier audio")
    video_path: str | None = Field(default=None, description="Chemin du fichier vidéo")
    storyboard: list[StoryboardSceneSchema] = Field(default_factory=list, description="Storyboard généré")
