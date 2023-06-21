from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

STATIC_DIR = Path("./static")
TEMPLATE_IMAGE = STATIC_DIR.joinpath(Path("./template.png"))
FONT_IMAGE = 35
FONT = ImageFont.truetype(
    str(STATIC_DIR.joinpath(Path("./Cleanvertising_Black.ttf")).absolute()),
    FONT_IMAGE
)

def generate_certificate(text: str) -> Image.Image:
    with Image.open(TEMPLATE_IMAGE) as image:
        draw = ImageDraw.Draw(image)
        text_wight = draw.textsize(text=text, font=FONT)
        image_wight = image.size
        text_position = (image_wight[0] - text_wight[0]) // 2, 620
        draw.text(text_position, text, font=FONT)

        return image
