from PIL import Image


def resize_image(in_path: str, out_path: str, allowed_dimensions: list[tuple[int, int]]):
    with Image.open(in_path) as img:
        width, height = img.size
        aspect_ratio = width / height
        best_dimension = min(allowed_dimensions, key=lambda d: abs(d[0]/d[1] - aspect_ratio))
        img_resized = img.resize(best_dimension, Image.LANCZOS)
        img_resized.save(out_path)
