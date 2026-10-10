"""Agent de génération d'images basé sur Replicate ou Stable Diffusion."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import replicate
except ImportError:
    replicate = None


class ImageGenerator:
    """Générateur d'images pour chaque scène du storyboard."""

    def __init__(
        self,
        output_dir: str = "output",
        api_key: str | None = None,
        provider: str = "replicate",
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        self.provider = provider

    def generate_for_storyboard(
        self,
        storyboard: List[Dict[str, Any]],
        output_prefix: str = "scene",
    ) -> List[Dict[str, Any]]:
        """Générer une image pour chaque scène du storyboard."""
        results = []

        for scene in storyboard:
            scene_num = scene.get("scene_number", 1)
            visual_prompt = scene.get("visual_prompt", "")
            output_name = f"{output_prefix}_{scene_num:03d}"

            try:
                image_path = self.generate(
                    prompt=visual_prompt,
                    output_name=output_name,
                )
                results.append(
                    {
                        "scene_number": scene_num,
                        "image_path": image_path,
                        "prompt": visual_prompt,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "scene_number": scene_num,
                        "image_path": None,
                        "error": str(e),
                    }
                )

        return results

    def generate(
        self,
        prompt: str,
        output_name: str = "image",
        width: int = 1280,
        height: int = 720,
    ) -> str:
        """Générer une image avec Replicate ou fallback."""
        if not prompt.strip():
            raise ValueError("Le prompt d'image est vide.")

        if self.provider == "replicate" and self.api_key and replicate:
            return self._generate_with_replicate(prompt, output_name, width, height)
        else:
            return self._generate_fallback(output_name, prompt)

    def _generate_with_replicate(
        self,
        prompt: str,
        output_name: str,
        width: int,
        height: int,
    ) -> str:
        """Générer avec Replicate API."""
        os.environ["REPLICATE_API_TOKEN"] = self.api_key

        output_path = self.output_dir / f"{output_name}.png"

        try:
            output = replicate.run(
                "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21aef33d3b3b0ce3e86",
                input={
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                    "num_outputs": 1,
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5,
                },
            )

            if output and len(output) > 0:
                import urllib.request
                urllib.request.urlretrieve(output[0], str(output_path))
                return str(output_path)
            else:
                raise ValueError("Replicate n'a pas généré d'image.")
        except Exception as e:
            raise RuntimeError(f"Erreur Replicate : {str(e)}")

    def _generate_fallback(
        self,
        output_name: str,
        prompt: str,
    ) -> str:
        """Créer une image de fallback avec Pillow."""
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            raise RuntimeError("Pillow n'est pas installé.")

        width, height = 1280, 720
        image = Image.new("RGB", (width, height), color=(20, 30, 50))
        draw = ImageDraw.Draw(image)

        # Dégradé de couleur
        for y in range(height):
            color_ratio = y / height
            r = int(20 + (60 - 20) * color_ratio)
            g = int(30 + (90 - 30) * color_ratio)
            b = int(50 + (150 - 50) * color_ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Texte
        draw.text(
            (40, 100),
            "VideoAgent Studio",
            fill=(255, 255, 255),
        )
        draw.text(
            (40, 200),
            f"Scène : {output_name}",
            fill=(200, 220, 255),
        )
        draw.text(
            (40, 350),
            prompt[:100],
            fill=(150, 180, 255),
        )

        output_path = self.output_dir / f"{output_name}.png"
        image.save(output_path, format="PNG")
        return str(output_path)


if __name__ == "__main__":
    generator = ImageGenerator(output_dir="output")
    image_path = generator.generate(
        prompt="Un bureau moderne avec des écrans d'ordinateur affichant de l'IA et de l'apprentissage automatique",
        output_name="test_scene_001",
    )
    print(f"Image générée : {image_path}")
