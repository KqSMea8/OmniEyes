# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:14:23 2017

@author: jamie
"""
import os
import cv2
import math
import sys

base_dir = os.path.dirname(os.path.realpath(__file__))
video_dir = os.path.join(base_dir, 'video')
image_dir = os.path.join(base_dir, 'image')

date = sys.argv[1]

def ProcessOneVideo(video_name, dir_name, extract_rate):
    vidcap = cv2.VideoCapture(video_name)
    frame_rate = vidcap.get(5)
    success,image = vidcap.read()
    count = 0
    success = True
    while success:
        frame_id = vidcap.get(1)
        success,image = vidcap.read()
        if frame_id % math.floor(frame_rate*extract_rate) == 0:             
            image_name = 'frame'+ str(count) + '.jpg'
            image_name = os.path.join(dir_name, image_name)
            cv2.imwrite(image_name, image)   
            count += 1
    
file_name = []
for (dirpath, dirnames, filenames) in os.walk(video_dir):
    file_name.extend(filenames)
    break

for f in file_name:
    if f.split('.')[1] == 'mp4':
        print('[INFO] Process ' + f)
        video_name = os.path.join(video_dir, f)
        dir_name = os.path.join(image_dir,date+'_'+f.split('.')[0])
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)    
        vidcap = cv2.VideoCapture(video_name)
        
        # EX : frame_rate=30 -> 30 frames per second
        frame_rate = vidcap.get(5)

        success,image = vidcap.read()
        count = 0
        success = True
        while success:
          frame_id = vidcap.get(1)
          success,image = vidcap.read()
          if frame_id % math.floor(frame_rate) == 0:             
              image_name = date + '_' + f.split('.')[0] + '_frame'+ str(count) + '.jpg'
              image_name = os.path.join(dir_name, image_name)
              cv2.imwrite(image_name, image)   
              count += 1
print('[INFO] Finish')