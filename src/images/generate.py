import base64
import os
import requests
from uuid import uuid4

from src.preprocessing.resize import resize_and_crop_image

allowed_dimensions = [
        (1024, 1024), (1152, 896), (1216, 832), (1344, 768), (1536, 640),
        (640, 1536), (768, 1344), (832, 1216), (896, 1152)
    ]

model_endpoint = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"
sdxl_sk = os.getenv('SDXL_SK', '')

BASE_STEP_COUNT = 30
BASE_IMAGE_STRENGTH = 0.8
STRENGTH_CREATIVITY_DAMPING = 0.65
CFG_SCALE = 5
STYLE_PRESET = "cinematic"


def generate_images(in_path: str, prompts, n_images_per_prompt: int, creativity: float, ) -> list:
    resized_path = in_path.split('.')[0] + '-resized-' + str(uuid4()) + '.png'
    resize_and_crop_image(in_path, resized_path, allowed_dimensions)

    generated_images = []

    for prompt in prompts:
        for i in range(n_images_per_prompt):
            response = requests.post(
                model_endpoint,
                headers={
                    "Accept": "application/json",
                    "Authorization": sdxl_sk
                },
                files={
                    "init_image": open(resized_path, "rb")
                },
                data={
                    "init_image_mode": "IMAGE_STRENGTH",
                    "image_strength": BASE_IMAGE_STRENGTH - (creativity * STRENGTH_CREATIVITY_DAMPING),
                    "steps": BASE_STEP_COUNT,
                    "seed": 0,
                    "cfg_scale": CFG_SCALE,
                    "samples": 1,
                    "style_preset": STYLE_PRESET,
                    "text_prompts[0][text]": prompt['generation_prompt'],
                    "text_prompts[0][weight]": 1,
                    "text_prompts[1][text]": prompt['negative_logits'],
                    "text_prompts[1][weight]": -1,
                }
            )

            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            data = response.json()

            if not os.path.exists("./out"):
                os.makedirs("./out")

            for _, image in enumerate(data["artifacts"]):
                file_path = f'./out/sdxl-{image["seed"]}-{i}.png'
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(image["base64"]))
                generated_images.append(file_path)

    os.remove(resized_path)

    return generated_images
