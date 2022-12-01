#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

from fontTools.ttLib import TTFont

TEXTS_DIR = "texts"
IMAGES_DIR = "images"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts a TTF font to PNG images with a given font size"
    )

    parser.add_argument(
        "font_path",
        help="The TTF font file to convert",
        type=str,
    )

    parser.add_argument(
        "font_size",
        help="The font size to use",
        type=int,
    )

    args = parser.parse_args()

    ttf_path = args.font_path
    font_size = args.font_size

    ttf_name, ttf_ext = os.path.splitext(os.path.basename(ttf_path))

    ttf_file = open(ttf_path, "rb")
    ttf = TTFont(
        ttf_file,
        0,
        allowVID=0,
        ignoreDecompileErrors=True,
        fontNumber=-1)

    for d in [TEXTS_DIR, IMAGES_DIR]:
        if not os.path.isdir(d):
            os.mkdir(d)

    for x in ttf["cmap"].tables:
        for y in x.cmap.items():
            char_unicode = chr(y[0])
            char_utf8 = char_unicode.encode('utf_8')
            char_name = y[1]
            try:
                decoded_char = char_utf8.decode('utf_8')
                f = open(os.path.join(TEXTS_DIR, char_name + '.txt'), 'w')
                f.write(decoded_char)
                f.close()
            except:
                print("Error decoding character: %s" % char_name)

    ttf.close()

    files = os.listdir(TEXTS_DIR)
    for filename in files:
        name, ext = os.path.splitext(filename)
        input_txt = TEXTS_DIR + "/" + filename
        output_png = IMAGES_DIR + "/" + ttf_name + \
            "_" + name + "_" + str(font_size) + ".png"

        subprocess.call([
            "magick",
            "-font", ttf_path,
            "-pointsize", str(font_size),
            "-background", "none",
            "label:@" + input_txt,
            output_png
        ])

    print("finished")
