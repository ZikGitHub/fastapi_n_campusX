from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get('/about')
def about():
    return {'message': "A Fully functional API to manage your patient records."}


@app.get('/view')
def view():
    data = load_data()

    return data

# path parameter
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient in DB", example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")


# query parameter
@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="Sort in ascending or descending order")):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field select from valid fields {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select between asc and desc")

    data = load_data()

    sorted_data = dict(sorted(data.items(), key=lambda x: x[1][sort_by], reverse=(order == 'desc')))

    return sorted_data


class CreatePatient(BaseModel):

    patient_id: Annotated[str, Field(..., description="ID of the patient in DB", example="P001")]
    name: Annotated[str, Field(..., description="Name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="City of the patient", example="New York")]
    age: Annotated[int, Field(..., description="Age of the patient", example=30)]
    height: Annotated[float, Field(..., description="Height of the patient", example=1.75)]
    weight: Annotated[float, Field(..., description="Weight of the patient", example=70.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)



@app.put('/create')
def create_patient(patient: CreatePatient):
    data = load_data()

    if patient.patient_id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.patient_id] = patient.model_dump()
    save_data(data)

    return patient.model_dump()











