import io
import os

import PIL.ImageOps
import pytesseract
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#############################################################

pytesseract.pytesseract.tesseract_cmd = r'C:\code\Tesseract-OCR\tesseract.exe'
ARKSCREENSHOTS = r'C:\games\Steam\userdata\54428735\760\remote\346110\screenshots'

# MAP = sys.argv[1]
# MODE = sys.argv[2]

# MAP = 'island.jpg'
MAP = 'valguero.jpg'
# MAP = 'crystal.jpg'
# MODE = 'one'


MODE = 'all'


#############################################################


def screenshot_processing(file):
    with open(f'{ARKSCREENSHOTS}\{file}', "rb") as f:
        image_bytes = f.read()

    image = Image.open(io.BytesIO(image_bytes))

    # вырезать
    box = (1103, 256, 1406, 806)
    image = image.crop(box)

    # image = image.convert('1')
    image = image.convert('L')
    image = PIL.ImageOps.invert(image)

    # image = image.resize((image.size[0] * 2, image.size[1] * 2))
    # image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # image.show()

    # распознать
    res = pytesseract.image_to_string(image, lang='eng', config='--psm 6 -c tessedit_char_whitelist=0123456789,')

    # print(res)
    # print(type(res))

    work = []

    for i in res.split('\n'):
        # print(i)
        lvl = i[:i.find(' ')]
        x = i[len(lvl) + 1:len(lvl) + 1 + i[len(lvl) + 1:].find(' ')]
        y = i[len(lvl) + len(x) + 2:]
        # print(lvl, x, y, '<')

        # if int(lvl) >= 140:
        #     work.append([int(lvl), int(x[:x.find(',')]), int(y[:y.find(',')])])
        try:
            work.append([int(lvl), int(x[:x.find(',')]), int(y[:y.find(',')])])
        except:
            pass

    # print(work)

    return work


def drawing_on_map(coord, draw_shadow=True):

    print(coord)

    for i in coord[::-1]:
        # font = ImageFont.truetype("arial.ttf", 20)
        font = ImageFont.truetype("arial.ttf", 30)
        # fontbg = ImageFont.truetype("arial.ttf", 40)

        print(i)

        lvl = i[0]
        x = i[1]
        y = i[2]

        txt = f'{lvl} {x} {y}'
        # txt = str(lvl) + str(x) + str(y)

        print(txt)

        # text_y = 40
        # text_x = 30

        text_y = 60
        text_x = 40

        shadow = 2

        if int(lvl) >= 140:
            collor = (255, 0, 0)
        elif int(lvl) >= 130:
            collor = (255, 255, 0)
        else:
            collor = (255, 255, 255)

        # точка
        ImageDraw.Draw(image_out).rectangle(
            # (y * 20, x * 20, (y + 1) * 20, (x + 1) * 20), outline='red', fill='red'
            (y * 20, x * 20, y * 20 + 5, x * 20 + 5), outline=(0, 0, 0), fill=collor
        )

        # тень
        if draw_shadow:
            ImageDraw.Draw(image_out).text((y * 20 - text_y - shadow, x * 20 - text_x), txt, (0, 0, 0), font=font)
            ImageDraw.Draw(image_out).text((y * 20 - text_y + shadow, x * 20 - text_x), txt, (0, 0, 0), font=font)
            ImageDraw.Draw(image_out).text((y * 20 - text_y, x * 20 - text_x - shadow), txt, (0, 0, 0), font=font)
            ImageDraw.Draw(image_out).text((y * 20 - text_y, x * 20 - text_x + shadow), txt, (0, 0, 0), font=font)

        # текст
        ImageDraw.Draw(image_out).text(
            # (y * 20 - 50, x * 20 - 70), txt, random.choice(collor16), font=font,
            (y * 20 - text_y, x * 20 - text_x), txt, collor, font=font,
        )

        # print(ImageDraw.Draw(image_out).textsize(txt, font=font))

        collor16 = [(000, 255, 255),
                    (000, 000, 255),
                    (255, 000, 255),
                    (128, 128, 128),
                    (000, 128, 000),
                    (000, 255, 000),
                    (128, 000, 000),
                    (000, 000, 128),
                    (128, 128, 000),
                    (128, 000, 128),
                    (255, 000, 000),
                    (192, 192, 192),
                    (000, 128, 128),
                    (255, 255, 255),
                    (255, 255, 000)]


def main():
    # files = os.listdir(os.getcwd())
    files = os.listdir(ARKSCREENSHOTS)

    print(files)

    if MODE == 'one':
        print('mode one')
        for i in range(len(files) - 1, -1, -1):
            # print(files[i])
            if files[i][-6:] == '_1.jpg':
                print(files[i])
                coord = screenshot_processing(files[i])
                drawing_on_map(coord, draw_shadow=True)
                break

    elif MODE == 'all':
        print('mode all')

        coord = []
        for file in files:
            if file[-6:] == '_1.jpg':
                for i in screenshot_processing(file):
                    if i not in coord:
                        coord.append(i)
        print(coord, type(coord))
        drawing_on_map(coord, draw_shadow=False)

        # try:
        # except:
        #     pass

    # отрисовка на карту

    # for i in sorted(work, key=lambda x: x[1]):
    # for i in work[::-1]:

    # image_out.show()

    image_out.save('out.jpg', "JPEG")

    os.system('explorer out.jpg')


#############################################################

if __name__ == "__main__":
    with open(MAP, "rb") as f:
        image_bytes = f.read()
    image_out = Image.open(io.BytesIO(image_bytes))

    main()

#############################################################
