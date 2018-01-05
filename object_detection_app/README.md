# object detection app

原始github https://github.com/datitran/object_detector_app

## 安裝方法

參考文件中的 object detection api 安裝
https://hackmd.io/IYdgbAZgnADCDGBaKAmArAI0QFjWgJogBwoCMAzImqTBkcAKbwxQQxA=

## 應該要有的packages

- tensorflow
- opencv (cv2)
- numpy 

## model
資料夾中附上的的是用7-11、紅綠燈訓練的model.pb 和 .pbtxt檔案
共兩個class

## 執行方式

細節看 object_detection_app.py 中的argparse argument

主要可以調整的參數 ： 

- --display_type : 有camera和video兩個選擇，預設是video
- --model_path : 訓練好的.pb檔案
- --label_path : object-detection.pbtxt 的路徑，預設就是資料夾中的這個，如果要改檔名或路徑記得這邊要改
- --num_classes : 總共有幾個class
- --video_path : 如果是用video的話要改定video路徑
- --width : 如果用camera的話，視訊寬度，預設480
- --height : 如果用camera的話，視訊高度，預設360

## 執行範例

用video (這邊沒附上影片檔，要用的話自己拿一個來測): 
:::info
python object_detection_app.py --model_path=model.pb --num_classes=2 --video_path=video.MP4
:::

用camera
:::info
python object_detection_app.py --display_type=camera --model_path=model.pb --num_classes=2
:::

執行中按Q可以結束程式



