# Font bitmap generator by John. 20170303
# Remember to add __future__ module later
# -*- coding: UTF-8 -*-
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import argparse, os

# Character size and canvas size.
char_s, canv_s, x, y = 64, 80, 0, 0

""" Check if characters set has been imported successfully. """
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# print(kanji[:10])

# Main function.
def ttf_to_bmp(kanji, font, char_size, canv_size, position_x, position_y):
    font_obj = ImageFont.truetype(font, char_size)
    bmp = list()
    i = 0
    for character in kanji:
        i += 1      
        # Create canvas and draw kanji on it.
        img = Image.new('L', (canv_size, canv_size), color=255)
        draw = ImageDraw.Draw(img) 
        tile = draw.text((position_x, position_y), character, font = font_obj, fill=0)
        # Convert IMAGE data into numpy array.
        bmp.append(np.asarray(img))
        img.close()
        del draw
    bmp = np.asarray(bmp)
    return bmp

if __name__ == "__main__":
    # Use argparser to define arguments necessary for this program.
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcefont", type=str, default=None,
                        help="Your source font file location.")
    parser.add_argument("--targetfont", type=str, default=None,
                        help="Your target font file location.")
    parser.add_argument("--saveto", type=str, default="font_array",
                        help="Directory to save converted font data.")
    parser.add_argument("--kanji", type=str, default=None,
                        help="Chinese characters set to apply calligraphy style.") 
    # Parse inputs into arguments and start processing.                             
    ARG = parser.parse_args()
    kanji = open(ARG.kanji, 'r', encoding='UTF-8').read()
    kanji = [x for x in kanji if x != '\n']
    if "sample_img" not in os.listdir(os.getcwd()):
        os.mkdir("sample_img")
    if ARG.saveto not in os.listdir(os.getcwd()):
        os.makedirs("font_array")
    if ARG.sourcefont:
        bmp = None
        bmp = ttf_to_bmp(kanji, ARG.sourcefont, char_s, canv_s, x, y)
        filename = os.path.join(ARG.saveto, "sourcefont.npy")
        print(bmp)
        print(bmp[0])
        print(bmp[0][0])
        np.save(filename, bmp)
        img = Image.fromarray(np.append([x for x in bmp[:100]], axis=1), 'RGB')
        img.save('sample_img/source.png')
    if ARG.targetfont:
        bmp = None   
        bmp = ttf_to_bmp(kanji, ARG.targetfont, char_s, canv_s, x, y)
        filename = os.path.join(ARG.saveto, "targetfont.npy")
        np.save(filename, bmp)
        img = Image.fromarray(bmp, 'RGB')
        img.save('sample_img/target.png')
