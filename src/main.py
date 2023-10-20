import asyncio
import logging

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from mangum import Mangum

from src.images.generate import generate_images
import zipfile
from pathlib import Path
import shutil

from src.prompts.generate import generate_prompts

app = FastAPI()
handler = Mangum(app)

logging.basicConfig(level=logging.INFO)


def remove_file(path: str):
    p = Path(path)
    if p.exists():
        p.unlink()


async def clean_files(zip_name: str, image_files: list, uploaded_image_path: str):
    await asyncio.sleep(60)
    remove_file(zip_name)
    remove_file(uploaded_image_path)
    for file in image_files:
        remove_file(file)


@app.post("/prompts")
async def create_prompts(prompt: str = Form(...)):
    return generate_prompts(in_sequence=prompt)


@app.post("/images")
async def create_images(
        background_tasks: BackgroundTasks,
        base_image: UploadFile,
        prompt: str = Form(...),
        images_per_variation: int = Form(1),
        creativity: float = Form(0.5)
):
    if creativity < 0.0 or creativity > 1.0:
        raise HTTPException(status_code=400, detail='Creativity must be a value between 0 and 1.')

    if not prompt:
        raise HTTPException(status_code=400, detail='Generation prompt must not be empty.')

    if images_per_variation < 1:
        raise HTTPException(status_code=400, detail='Invalid input for "images_per_variation".')

    if images_per_variation > 3:
        raise HTTPException(status_code=400, detail='The maximum amount of images per variation cannot be more than 3.')

    logging.info(f'Generating {images_per_variation} image(s) per variation for prompt: "{prompt}", creativity: {creativity}')

    image_gen_prompts = generate_prompts(prompt)

    try:
        image_path = Path(f"uploaded_images/{base_image.filename}")
        image_path.parent.mkdir(parents=True, exist_ok=True)
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(base_image.file, buffer)

        prompts = [{'generation_prompt': prompt, 'negative_logits': 'hands, bad food, disgusting, blurry, bad '
                                                                    'setting, glitches, bad plating, ugly cutlery,'
                                                                    'uneven plate, mismatched colors'} for prompt in image_gen_prompts]

        image_files = generate_images(str(image_path), prompts, images_per_variation, creativity)

        zip_name = "results.zip"
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for img_file in image_files:
                zipf.write(img_file, Path(img_file).name)

        background_tasks.add_task(clean_files, zip_name, image_files, str(image_path))

        return FileResponse(zip_name, media_type="application/zip")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

