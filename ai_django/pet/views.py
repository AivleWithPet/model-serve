from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import subprocess
import requests
import json
import os

def result(request):
    file = None
    access_token = None
    
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        pet_id = request.POST.get("pet_id")
        access_token = request.POST.get("token")
        
        # 리액트 - 장고 이미지 전송 확인 (정상)
        file_path = os.path.join("", file.name)
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        
        fs = FileSystemStorage()
        file_name = fs.save(file.name, file)
        
    # activate_cmd = f"conda activate copet"
    cd_cmd = "cd for_inference"
    
    command = f"python inf.py input_image/{file_name} configs/withpet/rtmdet_tiny_8xb32-300e_coco.py --weights checkpoints/epoch_7.pth --device cpu"
    process = subprocess.Popen(f"{cd_cmd} && {command}", stdout=subprocess.PIPE, shell=True)
    # process = subprocess.Popen(f"{activate_cmd} && {cd_cmd} && {command}", stdout=subprocess.PIPE, shell=True)
    process.communicate()
    
    file_name_split = file_name.rsplit('.', 1)[0] # 확장자 제거
    result_path = os.path.abspath(f'../ai_django/for_inference/outputs/preds/{file_name_split}.json')
    
    f = open(result_path)
    data = json.load(f)
    labels = data.get('labels')
    scores = data.get('scores')
    percentage = scores[0] * 100
    
    # files = {'imageFile': file}
    # files = {'imageFile': (file_name, file)}
    # files = {'imageFile': (file.name, file.read())}
    files = {'imageFile': open(file_path, 'rb')}
    data = {
        'petId': pet_id,
        'result': output(labels, scores),
        'percentage': percentage,
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        # 'Content-Type': 'multipart/form-data' #refreshpart에서는 필요 없음
    }

    url = 'http://localhost:8080/pet/result'
    
    response = requests.post(url, files= files, data=data, headers=headers)
    response_data = response.json()
    
    return JsonResponse({'result': response_data})

def output(labels, scores):

    category_names = ["증상없음", "각막궤양", "각막부골편", "결막염", "비궤양성각막염", "안검염"]
    max_idx = scores.index(max(scores))

    return category_names[labels[max_idx]]