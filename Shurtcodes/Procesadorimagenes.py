import numpy as np
from PIL import Image, ImageDraw, ImageFont

def GreyScaleImage(imagen=""):
    I = Image.open(imagen)
    I = I.convert('L') # convierte a escala de grises
    a = np.asarray(I, dtype=np.float32)
    Image.fromarray(a.astype(np.uint8)).save("GreyScale"+imagen)

def marqAqua(imagen="",texto="",color="white"):
    image = Image.open(imagen)
    draw = ImageDraw.Draw(image)
    # O bien /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf.
    font = ImageFont.truetype("jesto.otf", 200)
    lines = texto.splitlines()
    w = font.getsize(max(lines, key=lambda s: len(s)))[0]
    h = font.getsize(texto)[1] * len(lines)
    x, y = image.size
    x /= 2
    x -= w / 2
    y /= 2
    y -= h / 2
    draw.multiline_text((x, 50),text=texto, font=font, fill=color,align="center",)
    image.save("marte2.png")

#pruebas
GreyScaleImage("yeslytex.png")
marqAqua("yeslytex.png","Texto para probar bit",'#f2e3e3')



