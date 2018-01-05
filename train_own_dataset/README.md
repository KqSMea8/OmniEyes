# 訓練自己的dataset

原始github https://github.com/datitran/raccoon_dataset

## annotations

放所有的xml檔案

## images

放所有的照片檔案

## data

裡面有一個label_class.pbtxt，如果要增減class的話要修改這個檔案
記得id要從1開始算

## training

裡面是 .config檔案，詳細細節看文件
https://hackmd.io/IYdgbAZgnADCDGBaKAmArAI0QFjWgJogBwoCMAzImqTBkcAKbwxQQxA=

## data_preprocessing.py

用來把所有照片、xml檔案轉成 .record檔案和.csv

