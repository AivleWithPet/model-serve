from django.shortcuts import render
import pandas as pd
from . import get_result
from django.http import JsonResponse

def result(request):
    test = pd.DataFrame({'Sepal.Length':[10],
                  'Sepal.Width':[10],
                  'Petal.Length':[10],
                  'Petal.Width':[10]})
    prediction = get_result.prediction(test)
    data = {
        'prediction': prediction[0]
    }
    return JsonResponse(data)
