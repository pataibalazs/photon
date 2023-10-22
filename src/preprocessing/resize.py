from PIL import Image


def resize_and_crop_image(in_path: str, out_path: str, allowed_dimensions: list[tuple[int, int]]):
    with Image.open(in_path) as img:
        width, height = img.size
        aspect_ratio = width / height

        # Find the closest allowed dimensions
        best_dimension = min(allowed_dimensions, key=lambda d: abs(d[0]/d[1] - aspect_ratio))

        # Calculate the target aspect ratio
        target_aspect_ratio = best_dimension[0] / best_dimension[1]

        if aspect_ratio > target_aspect_ratio:
            # If the original aspect ratio is greater than the target one
            # we need to adjust the width of the image
            new_width = int(target_aspect_ratio * height)
            offset = (width - new_width) // 2
            crop_box = (offset, 0, width - offset, height)
        else:
            # If the original aspect ratio is less than the target one
            # we need to adjust the height of the image
            new_height = int(width / target_aspect_ratio)
            offset = (height - new_height) // 2
            crop_box = (0, offset, width, height - offset)

        # Crop and resize the image
        img_cropped = img.crop(crop_box)
        img_resized = img_cropped.resize(best_dimension, Image.LANCZOS)
        img_resized.save(out_path)

