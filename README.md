# VideoAgent Studio

Plateforme MVP d'automatisation de création de vidéos assistée par IA.

Objectif : générer un script, un story-board, une voix off et un rendu vidéo à partir d'une simple demande utilisateur.

## Ce que contient le projet

- Agent de script IA
- Agent de story-board
- Agent de synthèse vocale (TTS)
- Agent de rendu vidéo
- API FastAPI pour lancer la génération
- Sortie locale dans le dossier `output/`

## Stack technique

- Python 3.11+
- FastAPI
- Pydantic
- gTTS (TTS)
- Pillow
- FFmpeg (optionnel pour le rendu MP4)

## Démarrage rapide

1. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Installer les dépendances

```bash
pip install -r requirements.txt
```

3. Lancer l'API

```bash
uvicorn app.main:app --reload
```

4. Appeler l'API

```bash
curl -X POST http://127.0.0.1:8000/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Créer une vidéo de 30 secondes sur l'IA pour les PME",
    "duration": 30,
    "style": "cinematic",
    "language": "fr",
    "voice": "fr",
    "output_name": "ia_pme_demo"
  }'
```

## Endpoint principal

- POST `/api/generate-video`

### Paramètres

- `prompt` : idée générale de la vidéo
- `duration` : durée en secondes
- `style` : style visuel (cinematic, social, corporate, futuristic)
- `language` : langue de la voix (`fr`, `en`, etc.)
- `voice` : nom de voix ou config
- `output_name` : nom du fichier de sortie

## Sortie

Le pipeline produit un dossier dans `output/<output_name>/` contenant :

- `manifest.json`
- `poster.png`
- `voice.mp3` si la synthèse fonctionne
- `video.mp4` si FFmpeg est disponible

## Architecture du MVP

```text
app/
  __init__.py
  config.py
  main.py
  schemas.py
agents/
  __init__.py
  script_agent.py
  storyboard_agent.py
  voice_agent.py
  render_agent.py
workflows/
  video_pipeline.py
```

## À venir dans la version 2

- génération d'images par IA
- workflow multi-agent pour script, storyboard, montage et diffusion
- dashboard web
- intégration avec OpenAI/Claude/Gemini
- gestion de files de tâches et stockage cloud
- export automatique vers YouTube/TikTok/Reels

## Licence

MIT
