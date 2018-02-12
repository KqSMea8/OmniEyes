# Omni Eyes Dataset

標記教學文件 https://hackmd.io/IYJgJgDAbAnAjAZgLQDMCmMAcSAsAjTMJGHOKJQkYTAVhRQlJyA=
（文件原本是要教助理用的，用的是DELL筆電那台，路徑參考用就好）

## video

所有新拿到的行車記錄器影片放這

## old_video

當執行完 get_frame.py把video中的影片轉成frame之後，把video搬到這放
是怕教授突然需要舊的紀錄器影片，如果不用也是可以直接刪掉

## get_frame.py

執行時記得輸入執行當天的日期，例如

python get_frame.py 20180105

目的是避免行車記錄器影片名稱重複，導致之後要加入新資料時很麻煩

這個python檔會把video資料夾中，所有mp4檔名的檔案，用opencv每秒擷取一張frame，並存到image當中
（如果有非mp4檔名，記得去main裡面改）

假設影片名字是 PPG0001.mp4，會在image資料夾中產生20180105_PPG0001資料夾
裏面照片名字就是 20180105_PPG0001_frame0.jpg , .......

## copy_image.py

標記完成的資料夾我們要手動在名字前面加上'done_'
例如 20180105_PPG0001 -> done_20180105_PPG0001
這個python檔會把image資料夾當中，所有名字前綴是done_的，裏面所有有image和xml的檔案pair（有被標記的才會有xml）
複製到final_image和final_xml當中，以便訓練使用








