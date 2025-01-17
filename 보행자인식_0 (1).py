# -*- coding: utf-8 -*-
"""보행자인식_0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a8Bg4i1CZ_H1y9oPwn3oAoq26X1b0FL4
"""

from google.colab import drive
import os

drive.mount('/content/drive/')

# 작업 경로를 MyDrive로 변경하여 구글 드라이브에 접속 후 바로 작업 디렉토리를 확인 가능

print('현재 작업 경로 :', os.getcwd())
os.chdir('/content/drive/MyDrive')
print('변경된 작업 경로 :', os.getcwd())

# 처음에 한번만 실행 !
!git clone https://github.com/ultralytics/yolov5  # YOLOv5 레퍼지토리 clone

# Commented out IPython magic to ensure Python compatibility.
# 필요한 패키지 다운로드 및 임포트
# %cd yolov5
# %pip install -qr requirements.txt # install dependencies
# %pip install -q roboflow

import torch
import yaml
from IPython.display import Image, clear_output  # to display images

print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

# 사용할 데이터셋 경로 및 데이터셋의 yaml 파일 경로 지정
data_dir = '/content/drive/MyDrive/dataset/HumanRecognization'
data_yaml = '/content/drive/MyDrive/dataset/HumanRecognization/data.yaml'

# 데이터셋 yaml 파일 확인
with open(data_yaml) as f:
    film = yaml.load(f, Loader=yaml.FullLoader)
    display(film)

# yaml 파일의 train, val 데이터가 있는 경로 수정 (기존 경로 -> 구글 드라이브에 저장된 경로로)
film['train'] = '/content/drive/MyDrive/dataset/HumanRecognization/train/images'
film['test'] = '/content/drive/MyDrive/dataset/HumanRecognization/test/images'
film['val'] = '/content/drive/MyDrive/dataset/HumanRecognization/valid/images'

with open(data_yaml, 'w') as f: #write mode
    yaml.dump(film, f)

print('변경된 yaml 파일 :')
with open(data_yaml) as f: #read mode
    film = yaml.load(f, Loader=yaml.FullLoader)
    display(film)

#YOLOv5 모델 학습
 !python train.py --img 416 --batch 16 --epochs 150 --data {data_yaml} --weights yolov5s.pt --cache

# Commented out IPython magic to ensure Python compatibility.
# Start tensorboard
# Launch after you have started training
# logs save in the folder "runs"
# %load_ext tensorboard
# %tensorboard --logdir runs

# 테스트 이미지 경로
test_data_dir = film['val']

!python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.1 --source {test_data_dir}

import glob
from IPython.display import Image, display

test_exp_num = 2

if not os.path.exists('/content/drive/MyDrive/yolov5/runs/detect/exp' + str(test_exp_num) + '/') :
  raise Exception('test_exp_num 을 다시 확인하세요.')

for imageName in glob.glob('/content/drive/MyDrive/yolov5/runs/detect/exp' + str(test_exp_num) + '/*.jpg'): #assuming JPG
    display(Image(filename=imageName))
    print("\n")