import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = 73
HEIGHT_CM = 170
AGE = 30

today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": os.environ.get("APP_ID"),
    "x-app-key": os.environ.get("API_KEY"),
}

exercise_parameters = {
    "query": input("Tell me what exercises you do today? "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=exercise_endpoint, json=exercise_parameters, headers=headers)
exercise_data = exercise_response.json()["exercises"]

for exercise in exercise_data:
    sheety_parameters = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    headers = {"Authorization": f"Bearer {os.environ.get('TOKEN')}"}

    sheety_response = requests.post(url=os.environ.get("sheety_endpoint"), json=sheety_parameters, headers=headers)
    print(sheety_response.text)
