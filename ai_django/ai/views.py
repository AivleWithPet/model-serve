from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from . import get_result
import json
import requests

def result(request):
    data = {'Sepal.Length':[10],
            'Sepal.Width':[10],
            'Petal.Length':[10],
            'Petal.Width':[10]}
    
    data = pd.DataFrame(data)
    prediction = get_result.prediction(data)
    payload = {
        'prediction': prediction[0]
    }
    # headers = {'Content-Type': 'application/json'}
    url = 'http://localhost:8080/model_result'
    # json_data = json.dumps(data)  # 딕셔너리를 JSON 문자열로 변환
    response = requests.post(url, data=payload)
    
    # 응답의 JSON 데이터를 파싱하여 반환
    response_data = response.json()
    
    return JsonResponse(response_data)
    # 응답 확인
    # if response.status_code == 200:
    #     return JsonResponse({'message': '요청이 성공적으로 전송되었습니다.'})
    # else:
    #     return JsonResponse({'message': '요청 전송에 실패했습니다.', 'status_code': response.status_code})
