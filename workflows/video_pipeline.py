"""Pipeline complet de génération vidéo."""
import json
from typing import Any, Dict

from agents.script_agent import ScriptAgent


class VideoPipeline:
    """Orchestrateur principal du pipeline vidéo."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        """Initialiser le pipeline.
        
        Args:
            api_key: Clé API OpenAI
            model: Modèle à utiliser
        """
        self.script_agent = ScriptAgent(api_key=api_key, model=model)

    def generate(
        self,
        prompt: str,
        duration: int = 30,
        style: str = "cinematic",
        language: str = "fr",
    ) -> Dict[str, Any]:
        """Générer un script vidéo complet.
        
        Args:
            prompt: Sujet ou idée de la vidéo
            duration: Durée cible en secondes
            style: Style visuel
            language: Langue
            
        Returns:
            Script structuré prêt pour montage
        """
        return self.script_agent.generate(
            prompt=prompt,
            duration=duration,
            style=style,
            language=language,
        )

    def to_json(self, script: Dict[str, Any]) -> str:
        """Convertir un script en JSON."""
        return json.dumps(script, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Test du pipeline
    pipeline = VideoPipeline()
    result = pipeline.generate(
        prompt="Tutoriel sur l'apprentissage de Python",
        duration=45,
        style="social",
    )
    print(pipeline.to_json(result))
