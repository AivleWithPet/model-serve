from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import subprocess
import json
import os
import requests

def result(request):
    file = None
    access_token = None
    
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        pet_id = request.POST.get("pet_id")
        access_token = request.POST.get("token")
        
        fs = FileSystemStorage()
        fs.save('demo3.png', file)
        
    activate_cmd = f"conda activate copet"
    cd_cmd = "cd for_inference"
    
    command = "python inf.py input_image/demo3.png configs/withpet/rtmdet_tiny_8xb32-300e_coco.py --weights checkpoints/epoch_7.pth --device cpu"
    process = subprocess.Popen(f"{activate_cmd} && {cd_cmd} && {command}", stdout=subprocess.PIPE, shell=True)
    process.communicate()
    
    file_path = os.path.abspath('../ai_django/for_inference/outputs/preds/demo3.json')
    f = open(file_path)
    data = json.load(f)
    labels = data.get('labels')
    scores = data.get('scores')
    
    files = {'file': file}
    data = {
        'pet_id': pet_id,
        'disase_name': output(labels, scores)
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'multipart/form-data'
    }
    url = 'http://localhost:8080/pet/result'
    # response = requests.post(url, files= files, data=data, headers=headers)
    
    # # 응답의 JSON 데이터를 파싱하여 반환
    # response_data = response.json()
    
    # return JsonResponse({'result': response_data})
    
    return JsonResponse({'result': output(labels, scores)})

    # 응답 확인
    # if response.status_code == 200:
    #     return JsonResponse({'message': '요청이 성공적으로 전송되었습니다.'})
    # else:
    #     return JsonResponse({'message': '요청 전송에 실패했습니다.', 'status_code': response.status_code})


def output(labels, scores):

    category_names = ["증상없음", "각막궤양", "각막부골편", "결막염", "비궤양성각막염", "안검염"]

    max_idx = scores.index(max(scores))

    return category_names[labels[max_idx]]


def read_file():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'test.png')

    with open(file_path, 'rb') as file:
        file_content = file.read()

    return file_content
