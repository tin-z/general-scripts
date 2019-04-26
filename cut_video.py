#!/usr/bin/env python
import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
"""
 example usage: python3 ./cut_video.py path_file start_time end_time  #time format  HH:MM:SS
 output: OUTPUT_path_file
"""

def to_sec(time_format):
 ret = time_format.split(":")
 return int( ret[0] * 60 * 60 + ret[1] * 60 + ret[2] )

def main( args):
 if( len(args)  != 3): raise ValueError("example usage: python3 ./cut_video.py path_file start_time end_time  #time format  HH:MM:SS")
 name_path, start_time, end_time = args[0], args[1], args[2]
 try:
  ffmpeg_extract_subclip(name_path, to_sec(start_time), to_sec(end_time), target=( "{0}_{1}".format("OUTPUT", name_path)) )
 except :
  print("Some issue .. {} ".format(args)) 


if __name__ == "__main__":
  main(sys.argv[1:])
