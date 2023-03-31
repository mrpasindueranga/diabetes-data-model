from flask import Flask, send_from_directory, request
from flask_swagger_ui import get_swaggerui_blueprint
import pickle

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)

sample_dict = {
    "name": "Pasindu Eranga",
    "gender": "Male"
}

# Routes


@app.get("/my_details")
def my_details():
    return {"data": sample_dict}


@app.post("/predict")
def predict():
    data = request.get_json()
    glucose = data['glucose']
    blood_pressure = data['blood_pressure']
    skin_thickness = data['skin_thickness']
    insulin = data['insulin']
    bmi = data['bmi']
    dpf = data['dpf']
    age = data['age']
    print(data)
    return check_diabetes(glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age)


def check_diabetes(glucose: float, blood_pressure: float, skin_thickness: float, insulin: float, bmi: float, dpf: float, age: int):
    with open('model.pickle', 'rb') as f:
        model = pickle.load(f)
        if (model.predict([[glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]]))[0]:
            return {"data": "Diabetes Patient"}
        else:
            return {"data": "Non diabetes patient"}
