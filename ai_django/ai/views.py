from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from . import get_result
import json
import requests
import subprocess
import os
def result(request):
    activate_cmd = f"conda activate openmmlab"
    # subprocess.run(activate_cmd, shell=True)
    
    cd_cmd = "cd for_inference"
    # subprocess.run(cd_cmd,shell=True)
    
    command = "python inf.py input_image/demo3.png configs/withpet/rtmdet_tiny_8xb32-300e_coco.py --weights checkpoints/epoch_7.pth --device cpu"
    process = subprocess.Popen(f"{activate_cmd} && {cd_cmd} && {command}", stdout=subprocess.PIPE, shell=True)
    process.communicate()
    
    file_path = os.path.abspath('../ai_django/for_inference/outputs/preds/demo3.json')
    f = open(file_path)
    data = json.load(f)
    print(data.get('labels'))
    # headers = {'Content-Type': 'application/json'}
    # url = 'http://localhost:8080/model_result'
    # json_data = json.dumps(data)  # 딕셔너리를 JSON 문자열로 변환
    # response = requests.post(url, data=payload)
    
    # 응답의 JSON 데이터를 파싱하여 반환
    # response_data = response.json()
    
    return JsonResponse({'message': '요청이 성공적으로 전송되었습니다.'})
    # 응답 확인
    # if response.status_code == 200:
    #     return JsonResponse({'message': '요청이 성공적으로 전송되었습니다.'})
    # else:
    #     return JsonResponse({'message': '요청 전송에 실패했습니다.', 'status_code': response.status_code})
