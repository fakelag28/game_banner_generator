from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
import io
import requests
import imageio
import numpy as np

def generate_banner_image(nickname, position, discord_tag, url, resolution=(2560, 600), show_position=True, show_discord=True):
    width, height = resolution
    data = requests.get(url).content
    image = Image.open(io.BytesIO(data))
    banner = Image.new('RGB', (width, height), (255, 255, 255) if resolution == (2560, 600) else (0, 0, 0))
    background = ImageOps.fit(image, (width, height), method=Image.BICUBIC, centering=(0.5, 0.5))
    banner.paste(background, (0, 0))
    draw = ImageDraw.Draw(banner)
    font_path = os.path.join(os.path.dirname(__file__), 'arturito.ttf')

    fonts = {
        'nickname': ImageFont.truetype(font_path, size=125 if resolution == (2560, 600) else 95),
        'position': ImageFont.truetype(font_path, size=70 if resolution == (2560, 600) else 60),
        'discord': ImageFont.truetype(font_path, size=50 if resolution == (2560, 600) else 40)
    }

    positions = [(63, 150), (63, 275), (63, 350)] if resolution == (2560, 600) else [(width - 50, 100), (width - 50, 200), (width - 50, 270)]
    shadow_color, shadow_offset = (20, 20, 20), (7 if resolution == (2560, 600) else 5)

    elements = [(nickname, positions[0], fonts['nickname'])]
    if show_position: elements.append((position, positions[1], fonts['position']))
    if show_discord: elements.append((discord_tag, positions[2], fonts['discord']))

    for text, pos, font in elements:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        adjusted_pos = (pos[0] - (text_bbox[2] - text_bbox[0]), pos[1])
        shadow_text = Image.new('RGBA', banner.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_text)
        shadow_draw.text((adjusted_pos[0] + shadow_offset, adjusted_pos[1] + shadow_offset), text, font=font, fill=shadow_color)
        shadow_text = shadow_text.filter(ImageFilter.GaussianBlur(radius=shadow_offset))
        banner.paste(shadow_text, (0, 0), shadow_text)
        draw.text(adjusted_pos, text, font=font, fill=(255, 255, 255))

    banner.save('banner.png' if resolution == (2560, 600) else 'banner_2560x600.png')

def generate_banner_gif(nickname, position, discord_tag, url, resolution=(2560, 600), show_position=True, show_discord=True):
    data = requests.get(url).content
    gif = imageio.mimread(data)
    width, height = resolution
    frames = []

    for frame in gif:
        banner = Image.new('RGB', (width, height), (255, 255, 255) if resolution == (2560, 600) else (0, 0, 0))
        background = ImageOps.fit(Image.fromarray(frame), (width, height), method=Image.BICUBIC, centering=(0.5, 0.5))
        banner.paste(background, (0, 0))
        draw = ImageDraw.Draw(banner)
        font_path = os.path.join(os.path.dirname(__file__), 'arturito.ttf')

        fonts = {
            'nickname': ImageFont.truetype(font_path, size=60 if resolution == (2560, 600) else 70),
            'position': ImageFont.truetype(font_path, size=35 if resolution == (2560, 600) else 45),
            'discord': ImageFont.truetype(font_path, size=25 if resolution == (2560, 600) else 35)
        }

        positions = [(32, 75), (32, 137), (32, 175)] if resolution == (2560, 600) else [(width - 50, 100), (width -  50, 180), (width - 50, 240)]
        shadow_color, shadow_offset = (20, 20, 20), 4
        elements = [(nickname, positions[0], fonts['nickname'])]
        if show_position: elements.append((position, positions[1], fonts['position']))
        if show_discord: elements.append((discord_tag, positions[2], fonts['discord']))

        for text, pos, font in elements:
            shadow_text = Image.new('RGBA', banner.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_text)
            shadow_draw.text((pos[0] + shadow_offset, pos[1] + shadow_offset), text, font=font, fill=shadow_color)
            shadow_text = shadow_text.filter(ImageFilter.GaussianBlur(radius=shadow_offset))
            banner.paste(shadow_text, (0, 0), shadow_text)
            draw.text(pos, text, font=font, fill=(255, 255, 255))

        frames.append(np.array(banner))

    imageio.mimsave('banner.gif' if resolution == (2560, 600) else 'banner_2560x600.gif', frames, duration=0.2, optimize=True)

type = input('Выберите тип баннера (2560/600 - 1, Discord banner - 2): ')
nickname = input('Введите никнейм: ')
position = input('Введите должность/роль: ')
discord_tag = input('Введите Discord тэг: ')
url = input('Введите URL для заднего фона: ')
is_show_position = True
is_show_discord = False

if type == '2':
    if '.gif' in url:
        generate_banner_gif(nickname, position, discord_tag, url, resolution=(1360, 480), show_position=is_show_position, show_discord=is_show_discord)
    else:
        generate_banner_image(nickname, position, discord_tag, url, resolution=(1360, 480), show_position=is_show_position, show_discord=is_show_discord)
else:
    if '.gif' in url:
        generate_banner_gif(nickname, position, discord_tag, url)
    else:
        generate_banner_image(nickname, position, discord_tag, url)
print('Баннер успешно создан.')