# Démarrage rapide - VideoAgent Studio

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/DIOUF341/ai-video-automation-agents.git
cd ai-video-automation-agents
```

### 2. Créer un environnement virtuel
```bash
python -m venv .venv

# Sur Linux/Mac
source .venv/bin/activate

# Sur Windows
.venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API OpenAI
```

## Utilisation

### Option A : Via l'API FastAPI

#### Lancer le serveur
```bash
uvicorn app.main:app --reload
```

Le serveur démarre sur `http://localhost:8000`

#### Appel simple avec curl
```bash
curl -X POST http://localhost:8000/api/generate-script \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Créer une vidéo de 30 secondes sur l\'IA pour les PME",
    "duration": 30,
    "style": "cinematic",
    "language": "fr"
  }'
```

#### Accéder à la documentation interactive
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Option B : Via Python directement

#### Test du script agent
```python
from agents.script_agent import ScriptAgent
import json

agent = ScriptAgent()
script = agent.generate(
    prompt="Tutoriel sur Python",
    duration=30,
    style="social",
    language="fr"
)

print(json.dumps(script, ensure_ascii=False, indent=2))
```

#### Test du pipeline
```python
from workflows.video_pipeline import VideoPipeline

pipeline = VideoPipeline()
result = pipeline.generate(
    prompt="Comment vendre en ligne",
    duration=45,
    style="corporate"
)

print(pipeline.to_json(result))
```

## Structure du projet

```
ai-video-automation-agents/
├── agents/
│   ├── __init__.py
│   └── script_agent.py          # Agent de génération de script IA
├── app/
│   ├── __init__.py
│   ├── main.py                  # API FastAPI
│   ├── schemas.py               # Schémas Pydantic
│   └── config.py                # Configuration
├── workflows/
│   ├── __init__.py
│   └── video_pipeline.py        # Pipeline d'orchestration
├── requirements.txt             # Dépendances Python
├── .env.example                 # Variables d'environnement
├── README.md                    # Documentation principale
└── QUICKSTART.md               # Ce fichier
```

## Paramètres disponibles

### Styles visuels
- `cinematic`: Cinématographique, dramatique
- `social`: Réseaux sociaux, dynamique
- `corporate`: Professionnel, corporate

### Langues supportées
- `fr`: Français
- `en`: Anglais
- `es`: Espagnol
- `de`: Allemand

## Résultat attendu

Le script généré contient:

```json
{
  "title": "Titre de la vidéo",
  "summary": "Résumé du contenu",
  "duration_seconds": 30,
  "style": "cinematic",
  "language": "fr",
  "scenes": [
    {
      "title": "Scène 1",
      "visual": "Description visuelle",
      "narration": "Texte à dire",
      "duration": 10
    }
  ],
  "voiceover": "Narration générale"
}
```

## Prochaines étapes

1. ✅ Script IA (complété)
2. ⏳ Agent de voix off
3. ⏳ Générateur de visuels
4. ⏳ Montage vidéo
5. ⏳ Interface web

## Dépannage

### Erreur: "No module named 'openai'"
```bash
pip install openai
```

### Erreur: "OPENAI_API_KEY not found"
Assurez-vous que la clé API est définie dans `.env` ou en variable d'environnement.

### L'API ne démarre pas
```bash
# Vérifier que le port 8000 est disponible
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

## Support

Pour les problèmes, ouvrez une issue sur GitHub:
https://github.com/DIOUF341/ai-video-automation-agents/issues
