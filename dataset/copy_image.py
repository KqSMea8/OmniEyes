# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:14:23 2017

@author: jamie
"""
import os
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--dir_path", help="path of all of the dirs")
parser.add_argument("--output_img", help="output images path")
parser.add_argument("--output_xml", help="output xmls path")
args = parser.parse_args()
    
dir_name = []
for (dirpath, dirnames, filenames) in os.walk(args.dir_path):
    dir_name.extend(dirnames)
    break

for d in dir_name:
    if 'done_' in d:
        print('[INFO] Process ' + d)
        file_name = []
        d = os.path.join(args.dir_path, d)
        for (dirpath, dirnames, filenames) in os.walk(d):
            file_name.extend(filenames)
            break
        for f in file_name:
            if f.split('.')[1] == 'xml':
                image = os.path.join(d, f.split('.')[0]+'.jpg')
                xml = os.path.join(d, f.split('.')[0]+'.xml')
                shutil.copyfile(image, os.path.join(args.output_img, f.split('.')[0]+'.jpg'))
                shutil.copyfile(xml, os.path.join(args.output_img, f.split('.')[0]+'.xml'))