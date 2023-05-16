import os
import joblib

def prediction(input):
    model_file = 'model_iris.pkl'
    model_path = os.path.join(os.path.dirname(__file__), model_file)
    
    model = joblib.load(model_path)    
    
    prediction = model.predict(input)
    
    return prediction