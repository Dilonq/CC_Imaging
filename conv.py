from PIL import Image
import numpy as np

import os

import textwrap

# w = input("Width (max 164): ")
# h = input("Height (max 81): ")
w = h = ""
if w == "":
    w = 164
if h == "":
    h = 81

name = input("Filename: ")

# dit = input("Dither (y/n): ").lower()
# dit = False
# if dit == "y":
#     dit = True

def RGB2Dec(rgb):
    rgb_tuple = rgb
    return rgb_tuple[0] << 16 | rgb_tuple[1] << 8 | rgb_tuple[2]

def _quantize_with_colors(image, colors, dither=0):
    pal_im = Image.new("P", (1, 1))
    color_vals = []
    for color in colors:
        for val in color:
            color_vals.append(val)
    color_vals = tuple(color_vals)
    pal_im.putpalette(color_vals + colors[-1] * (256 - len(colors)))
    image = image.convert(mode="RGB")
    return image.quantize(palette=pal_im,dither=dither)

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering

    # Really old versions of Pillow (before 4.x) have _new
    # under a different name
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)


# below is the old palette converter
# v
# hexdata = [ # default computercraft colors
#     "F0F0F0",
#     "F2B233",
#     "E57FD8",
#     "99B2F2",
#     "DEDE6C",
#     "7FCC19",
#     "F2B2CC",
#     "F2B2CC",
#     "999999",
#     "4C99B2",
#     "B266E5",
#     "3366CC",
#     "7F664C",
#     "57A64E",
#     "CC4C4C",
#     "191919"
# ]
#
# palettedata = []
#
# for i in range(len(hexdata)):
#     for ii in range(3):
#         palettedata.append(int(textwrap.wrap(hexdata[i], 2)[ii], 16))
#
# # Fill the entire palette so that no entries in Pillow's
# # default palette for P images can interfere with conversion
# NUM_ENTRIES_IN_PILLOW_PALETTE = 256
# num_bands = len("RGB")
# num_entries_in_palettedata = len(palettedata) // num_bands
# palettedata.extend(palettedata[:num_bands]
#                    * (NUM_ENTRIES_IN_PILLOW_PALETTE
#                       - num_entries_in_palettedata))
# # Create a palette image whose size does not matter
# arbitrary_size = 16, 16
# palimage = Image.new('P', arbitrary_size)
# palimage.putpalette(palettedata)





def cropDims(img, area):
    if area == "tl":
        t = 0
        l = 0
        r,b = img.size
        r = r/2
        b = b/2
    elif area == "tr":
        t = 0
        l, b = img.size
        l = l/2
        b = b/2
        r = l*2
    elif area == "bl":
        l = 0
        r,t = img.size
        t = t/2
        r = r/2
        b = t*2
    elif area == "br":
        l,t = img.size
        t = t/2
        l = l/2
        b = t*2
        r = l*2

    return img.crop((l,t,r,b))

def img_to_nfp(im, pal, dither=0):
    # most of the following code is from: https://github.com/DownrightNifty/computercraft-stuff/blob/master/nfp.py

    data = list(im.getdata().convert("RGB"))
    for i in range(len(data)):
        data[i] = RGB2Dec(data[i])

    print(data)

    width, height = im.size

    nfp_im = ""
    index = 0
    for row in range(height):
        for col in range(width):

            index += 1

            # convert 0-15 decimal value to hex string (0-f)

            # print("X:{}".format(row) + "Y: {}".format(col) + str(data_2d[row][col]))

            try:
                data[index]
            except:
                break

            for i in range(len(pal)):
                if int(pal[i]) == int(data[index]):
                    nfp_im += str(hex(i))[2:]
                    break

        nfp_im += "\n"
    return nfp_im



# actual conversion

image = Image.open(name)

colorCount = 16

image = image.convert('P', palette=Image.ADAPTIVE, colors=colorCount)

imageBig = image.resize((w*2,h*2), Image.ANTIALIAS)
image = image.resize((w,h), Image.ANTIALIAS)

imgColors = []

im = image
if im.mode=='P':
    colours = im.getcolors()

    palette = im.getpalette()
    for i in range(colorCount):
        r = palette[3*i]
        g = palette[3*i+1]
        b = palette[3*i+2]
        rgb = (r,g,b)

        imgColors.append(RGB2Dec(rgb))

# image = quantizetopalette(image, palimage, dither=dit)
# imageBig = quantizetopalette(imageBig, palimage, dither=dit)

# make new directory for files to go into
directory = name[:-4]
path = os.path.join(os.getcwd(), directory)
try:
    os.mkdir(path)
except:
    pass

f = open(name[:-4] + "/" + name[:-4] + ".nfp", "w")
f.write(img_to_nfp(image, imgColors))
f.close()

sections = ["tl","tr","bl","br"]
for i in range(4):
    imagePart = cropDims(imageBig, sections[i])
    f = open(name[:-4] + "/" + name[:-4] + "_" + sections[i] + ".nfp", "w")
    f.write(img_to_nfp(imagePart, imgColors))
    f.close()


# add in the lua file to change color palette
luaFile = ""

print(imgColors)
for i in range(len(imgColors)):
    luaFile += "term.setPaletteColor(" + str(2**i) + ", " + str(imgColors[i]) + ")\n"

f = open(name[:-4] + "/colorchanger.lua", "w")
f.write(luaFile)
f.close()
