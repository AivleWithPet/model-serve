from django.http import JsonResponse
import subprocess
import json
import os
from django.core.files.storage import FileSystemStorage

def result(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        token = request.POST.get("token")
        
        # fs = FileSystemStorage('/')
        # filename = fs.save(file.name, file)
        # file_url = fs.url(filename)
    
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
    print(print_output(labels, scores))


    # headers = {'Content-Type': 'application/json'}
    # url = 'http://localhost:8080/pet/result'
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


def print_output(labels, scores):

    category_names = ["증상없음", "각막궤양", "각막부골편", "결막염", "비궤양성각막염", "안검염"]

    max_idx = scores.index(max(scores))

    return category_names[labels[max_idx]]