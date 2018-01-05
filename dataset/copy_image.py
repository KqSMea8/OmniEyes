# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:14:23 2017

@author: jamie
"""
import os
import shutil

base_dir = os.path.dirname(os.path.realpath(__file__))
image_dir = os.path.join(base_dir, 'image')
final_image_dir = os.path.join(base_dir,'final_image')
final_xml_dir = os.path.join(base_dir,'final_xml')
    
dir_name = []
for (dirpath, dirnames, filenames) in os.walk(image_dir):
    dir_name.extend(dirnames)
    break

for d in dir_name:
    if 'done_' in d:
        print('[INFO] Process ' + d)
        file_name = []
        d = os.path.join(image_dir, d)
        for (dirpath, dirnames, filenames) in os.walk(d):
            file_name.extend(filenames)
            break
        for f in file_name:
            if f.split('.')[1] == 'xml':
                image = os.path.join(d, f.split('.')[0]+'.jpg')
                xml = os.path.join(d, f.split('.')[0]+'.xml')
                shutil.copyfile(image, os.path.join(final_image_dir, f.split('.')[0]+'.jpg'))
                shutil.copyfile(xml, os.path.join(final_xml_dir, f.split('.')[0]+'.xml'))