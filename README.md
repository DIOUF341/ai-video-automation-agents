# VideoAgent Studio

## Description
Ce projet sert à générer des vidéos courtes assistées par IA à partir d'un prompt.

## Lancer le backend
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Ouvrir l'interface web
Ouvrir le fichier `index.html` dans le navigateur.

Le frontend communique avec l'API sur `http://localhost:8000`.

## Endpoint principal
```bash
curl -X POST http://localhost:8000/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Créer une vidéo sur l'IA pour les PME",
    "duration": 30,
    "style": "cinematic",
    "language": "fr",
    "output_name": "demo_video"
  }'
```
