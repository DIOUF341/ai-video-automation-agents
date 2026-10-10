import json
import os
import re
from typing import Any, Dict, List

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


class ScriptAgent:
    """Agent IA pour générer des scripts vidéo."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        """Initialiser l'agent de script.
        
        Args:
            api_key: Clé API OpenAI (optionnel, cherche OPENAI_API_KEY en env)
            model: Modèle à utiliser (optionnel, défaut: gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if OpenAI and self.api_key else None

    def generate(
        self,
        prompt: str,
        duration: int = 30,
        style: str = "cinematic",
        language: str = "fr",
    ) -> Dict[str, Any]:
        """Générer un script vidéo.
        
        Args:
            prompt: Sujet ou idée de la vidéo
            duration: Durée cible en secondes
            style: Style visuel (cinematic, social, corporate)
            language: Langue de la voix off
            
        Returns:
            Dict avec titre, scènes, narration, etc.
        """
        if self.client is not None:
            return self._generate_with_openai(prompt, duration, style, language)
        return self._generate_fallback(prompt, duration, style, language)

    def _generate_with_openai(
        self,
        prompt: str,
        duration: int,
        style: str,
        language: str,
    ) -> Dict[str, Any]:
        """Générer avec OpenAI API."""
        system_prompt = (
            "Tu es un scénariste IA expert pour la création de vidéos courtes. "
            "Rédige la réponse en JSON valide avec uniquement les clés suivantes : "
            "title, summary, duration_seconds, style, language, scenes, voiceover. "
            "Chaque scène doit avoir : title, visual, narration, duration. "
            "Le format doit être compréhensible par un moteur de montage vidéo."
        )

        user_prompt = (
            f"Produit un script vidéo pour la demande suivante. "
            f"Prompt : {prompt}. "
            f"Durée cible : {duration} secondes. "
            f"Style visuel : {style}. "
            f"Langue : {language}. "
            "Rends le résultat prêt à être utilisé pour générer une voix off et des plans visuels."
        )

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        content = completion.choices[0].message.content
        if not content:
            raise ValueError("La génération IA n'a retourné aucun contenu.")

        payload = json.loads(content)
        payload["duration_seconds"] = int(payload.get("duration_seconds", duration))
        payload["style"] = style
        payload["language"] = language
        return payload

    def _generate_fallback(
        self,
        prompt: str,
        duration: int,
        style: str,
        language: str,
    ) -> Dict[str, Any]:
        """Générer sans API (mode fallback)."""
        cleaned_prompt = prompt.strip()
        title = self._slugify(cleaned_prompt[:52]) if cleaned_prompt else "Vidéo IA"

        # Calculer le nombre de scènes
        scene_count = max(3, min(6, duration // 8))
        scene_duration = max(6, duration // scene_count)
        remaining = duration - (scene_duration * scene_count)

        scenes: List[Dict[str, Any]] = []
        for i in range(scene_count):
            scene_len = scene_duration + (1 if i < remaining else 0)
            scenes.append(
                {
                    "title": f"Scène {i + 1}",
                    "visual": self._scene_visual(i, style, cleaned_prompt),
                    "narration": self._scene_narration(i, cleaned_prompt, style),
                    "duration": scene_len,
                }
            )

        voiceover = (
            f"Bienvenue dans cette vidéo sur {cleaned_prompt}. "
            f"Nous allons explorer le sujet avec un angle clair, dynamique et orienté vers l'action. "
            f"Chaque scène donne du sens, de la valeur et une vision forte pour captiver l'audience."
        )

        return {
            "title": title,
            "summary": (
                f"Vidéo générée automatiquement à partir du prompt : {cleaned_prompt}. "
                f"Style visuel : {style}."
            ),
            "duration_seconds": duration,
            "style": style,
            "language": language,
            "scenes": scenes,
            "voiceover": voiceover,
        }

    def _scene_visual(self, index: int, style: str, prompt: str) -> str:
        """Générer une description visuelle pour une scène."""
        visuals = {
            "cinematic": [
                "plan large avec lumière dramatique",
                "gros plan sur le sujet principal",
                "vue panoramique dynamique",
                "transition visuelle élégante",
                "mise en scène premium",
                "plan final imposant",
            ],
            "social": [
                "frame vertical énergique",
                "plan très dynamique pour réseaux sociaux",
                "image moderne et immersive",
                "montage rapide et punchy",
                "vision courte et impactante",
                "fin sur un message fort",
            ],
            "corporate": [
                "mise en scène professionnelle",
                "plan sobre et structuré",
                "présentation claire de la solution",
                "vue élégante sur le produit",
                "démonstration d'impact",
                "fin sur une conclusion de confiance",
            ],
        }

        pool = visuals.get(style, visuals["cinematic"])
        return f"{pool[index % len(pool)]} pour '{prompt[:40]}'."

    def _scene_narration(self, index: int, prompt: str, style: str) -> str:
        """Générer une narration pour une scène."""
        phrases = [
            f"Nous commençons par introduire le sujet principal : {prompt}.",
            "Cette idée apporte une réelle valeur et un cadre clair pour le public.",
            "Ensuite, nous mettons en avant les bénéfices concrets et l'impact attendu.",
            "L'objectif est de captiver l'attention dès les premières secondes.",
            "Le message devient plus fort avec une démonstration simple et visible.",
            "Nous terminons avec un appel à l'action clair et mémorable.",
        ]
        return phrases[index % len(phrases)]

    @staticmethod
    def _slugify(value: str) -> str:
        """Convertir un texte en slug."""
        value = re.sub(r"[^a-zA-Z0-9\s-]", "", value)
        value = re.sub(r"\s+", " ", value).strip()
        return value[:45].strip() or "Video_IA"


if __name__ == "__main__":
    # Test local du script agent
    agent = ScriptAgent()
    script = agent.generate(
        "Vidéo sur l'IA dans les PME",
        duration=30,
        style="cinematic",
        language="fr",
    )
    print(json.dumps(script, ensure_ascii=False, indent=2))
