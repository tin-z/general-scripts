#!/usr/bin/env python
import sys, os
from PIL import Image
from natsort import natsorted
"""
 take all *.jpg file in the working directory, then split them symmetrically by their height and past it in a new image
 example usage: python3 ./crop_symmetric.py width height
"""

def main( args):
 if( len(args)  != 2): raise ValueError("example usage: python3 ./crop_symmetric.py width height")
 width = int(args[0]) #1700
 height = int(args[1]) // 2 #1169
 images_input = [ Image.open(x) for x in natsorted( [ x  for x in os.listdir("./") if x.endswith("jpg") ]) ]
 images_output = []
 counter=0
 path="./output"
 os.makedirs(path, exist_ok=True)
 for i in range(0, len(images_input), 2):
  if (i+1) >= len(images_input):
    images_input[i].save( "{0}/output{1}.jpg".format(path, counter))
    break
  area1, area2 = ( 0, 0, width, height), ( 0, 0, width, height)
  cropped_image1, cropped_image2 = images_input[i].crop(area1), images_input[i+1].crop(area2)
  cropped_image3 = Image.new('RGBA', (width, height*2), (255, 255, 255, 255)) 
  cropped_image3.paste(cropped_image1, box=(0,0)); cropped_image3.paste(cropped_image2, box=(0, height))
  cropped_image3 = cropped_image3.convert('RGB')
  cropped_image3.save("{0}/output{1}.jpg".format(path,counter))
  counter += 1

if __name__ == "__main__":
  main(sys.argv[1:])
