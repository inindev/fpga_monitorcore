#!/usr/bin/python3

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

S=8
logocolor = (30, 150, 220)
fontname = 'RussoOne-Regular.ttf'

def draw_logo():
    image = Image.new('RGB', (256*S, 256*S), color = (0, 0, 0))
    fnt = ImageFont.truetype(fontname, 15*S)
    usr = ImageDraw.Draw(image)

    usr.text((2*S, 0), "SMSTang", fill=logocolor, font=fnt)

    # image.save('logo.png')
    left=13
    top=25
    image = image.crop((left, top, left+72*S, top+14*S))
    return image

def get_logo_data(image):
    #################################################
    # Convert image to grayscale
    gray = image.convert('L')

    # Initialize empty list for logo data
    logo_data = []

    # Set threshold to half of S*S
    threshold = (S * S) // 2

    # Process each 14x72 grid
    for y in range(0, 14*S, S):
        row = ""
        for x in range(0, 72*S, S):
            # Count white pixels in SxS block
            white_count = 0
            for i in range(S):
                for j in range(S):
                    if gray.getpixel((x + j, y + i)) > 50:
                        white_count += 1
            # Append 1 or 0 based on threshold
            if white_count > threshold:
                row += "1"
            else:
                row += "0"
        logo_data.append(row)
    return logo_data

def save_rows(logo_data, filename):
    assert len(logo_data) == 14 and all(len(row) == 72 for row in logo_data)
    with open(filename, 'w') as f:
        f.write("\n".join(logo_data) + "\n")


def save_preview(image, filename):
    #######################################################
    # Output logo.png for preview
    usr = ImageDraw.Draw(image)
    gridcolor = (50, 50, 50)
    coordcolor = (130, 130, 130)

    # Draw vertical grid lines
    for i in range(0, 72*S, S):
        usr.line((i, 0, i, 14*S), fill=gridcolor, width=1)

    # Draw horizontal grid lines  
    for i in range(0, 14*S, S):
        usr.line((0, i, 72*S, i), fill=gridcolor, width=1)

    # Draw numbers in first row
    fnt2 = ImageFont.truetype(fontname, S)
    for i in range(72):
        x = i * S + 2
        y = 0
        usr.text((x, y), str(i % 10), fill=coordcolor, font=fnt2)

    # Draw numbers in first column
    for i in range(14):
        x = 2
        y = i * S
        usr.text((x, y), str(i % 10), fill=coordcolor, font=fnt2)

    # Draw BGR5 color value in bottom right corner
    bgr5 = (logocolor[2] >> 3) << 10 | (logocolor[1] >> 3) << 5 | (logocolor[0] >> 3)
    x = 72*S - 100
    y = 14*S - S
    usr.text((x, y), f"BGR5: {bgr5:015b}", fill=coordcolor, font=fnt2)

    image.save(filename)
    # image.crop((0, 10, 72*S, 14*S)).resize((72,14)).convert('1').save('logo.png')


image = draw_logo()

logo_data = get_logo_data(image)

# Print logo data: 72*14
for row in logo_data:
    print(row)

# The rows go into a core's `iosys/gowin_dpb_menu.v` through tangcore's font script
save_rows(logo_data, 'logo.txt')
print("\nLogo saved as `logo.txt`. To use it for a core, from the tangcore folder:\n")
print("    scripts/font_glyphs.py --logo <core> logo.txt      (e.g. fpga_smstang)")

print("\nA preview of the logo is saved as `logo.png`.")
save_preview(image, 'logo.png')
