from PIL import Image


def place_runes(image, response):
    x = 0
    if "runeSlots" not in response:
        return image
    for rune_name in response["runeSlots"]:
        for _ in range(response["runeSlots"][rune_name]):
            rune = Image.open(f"death_knight/{rune_name}.png").convert("RGBA")
            rune = rune.resize((200, 200))

            image.paste(rune, (1200 + x, 2120), mask=rune)
            x += 200

    return image
