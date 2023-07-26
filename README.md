## 시작하기

### Requirements
- [anaconda](https://www.anaconda.com/download)
- [vscode](https://code.visualstudio.com/download)

### Installation
``` bash
$ git clone https://github.com/AivleWithPet/model-serve.git
```

1. vscode를 실행하고 클론해온 프로젝트를 열어줍니다.
2. 현재 경로가 <strong>model_serve/</strong> 인지 확인합니다.
3. terminal을 열고 cmd 창으로 전환합니다.


#### 📌 가상환경 생성 및 접속
``` 
$ conda create -n copet python=3.8 -y
$ conda activate copet
```

#### 📌 패키지 설치
```
$ pip install -r requirements.txt

$ conda install pytorch torchvision -c pytorch
$ conda install -c conda-forge pycocotools

$ pip install -U openmim

$ mim install mmengine
$ mim install "mmcv>=2.0.0"

$ cd ai_django
$ git clone https://github.com/open-mmlab/mmdetection.git
$ cd mmdetection
$ pip install -v -e .

$ mim download mmdet --config rtmdet_tiny_8xb32-300e_coco --dest .
```

#### 📌 Run a Django Server 🎉
```
$ cd ../ai_django/
$ python manage.py runserver
```
