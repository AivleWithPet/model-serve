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
        
        fs = FileSystemStorage()
        file_name = fs.save(file.name, file)
        
    # activate_cmd = f"conda activate copet"
    cd_cmd = "cd for_inference"
    
    command = f"python inf.py input_image/{file_name} configs/withpet/rtmdet_tiny_8xb32-300e_coco.py --weights checkpoints/epoch_7.pth --device cpu"
    process = subprocess.Popen(f"{cd_cmd} && {command}", stdout=subprocess.PIPE, shell=True)
    # process = subprocess.Popen(f"{activate_cmd} && {cd_cmd} && {command}", stdout=subprocess.PIPE, shell=True)
    process.communicate()
    
    file_name_split = file_name.rsplit('.', 1)[0] # 확장자 제거
    file_path = os.path.abspath(f'../ai_django/for_inference/outputs/preds/{file_name_split}.json')
    
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
    
    response = requests.post(url, files= files, data=data, headers=headers)
    response_data = response.json()
    
    return JsonResponse({'result': response_data})
    # return JsonResponse({'result': output(labels, scores)})

def output(labels, scores):

    category_names = ["증상없음", "각막궤양", "각막부골편", "결막염", "비궤양성각막염", "안검염"]
    max_idx = scores.index(max(scores))

    return category_names[labels[max_idx]]