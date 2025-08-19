import pyheif
from PIL import Image
from io import BytesIO

def convert_heic_bytes_to_image(image_bytes: bytes) -> Image.Image:
    heif_file = pyheif.read_heif(image_bytes)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        0,
        1,
    )
    return image
