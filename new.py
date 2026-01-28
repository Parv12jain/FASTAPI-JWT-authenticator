from fastapi  import FastAPI,HTTPException
import os
import joblib
from pydantic import BaseModel,Field,field_validator
from typing import Optional
import pandas as pd

app = FastAPI(title="Customer Churn Prediction API",
              description="An API to predict  customer churn")

@app.get('/') # this is get method and root endpoint
def greet():
    return {'message' : 'Whats up'}


# ye apn ne model path wale variable capital me isliye bana hai kyuki ab woh constant variable ban gya hai usko aage jakar koi bhi change nahi kr skta
MODEL_PATH = "best_balanced_churn_model.pkl" 

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at{MODEL_PATH}")

model = joblib.load(MODEL_PATH) # loading the model 


# CREATING THE PYDANTIC MODEL

# input schema(validation)

# class CustomerData(BaseModel):
#      #api ki language me ye columns ko field bolte hai
#     Gender:str = Field(...,example="Male") #...-> compulsory field
#     Age: int = Field(...,ge=18,le=100,examples=45) # ge-> greater than equal to, le -> less tha equal to
#     Tenure : int = Field(...,ge = 0, le = 100, example=12)
#     Service_Subscribed : int = Field(...,ge = 0, le = 10, example=12)
#     Contract_Type : str = Field(...,example="Month-to-Month")
#     MonthlyCharges : str = Field(...,gt=0, example=70.5) #gt -> greater than
#     TotalCharges : float = Field(...,ge=0,example=500.75)
#     TechSupport : str  = Field(...,example="YES")
#     OnlineSecurity : str = Field(...,example="YES")
#     InternetSecurity : str = Field(...,example="Fiber optic")


class CustomerData(BaseModel):
    Gender: str = Field(..., example="Male")

    Age: int = Field(
        ..., ge=18, le=100, example=45
    )

    Tenure: int = Field(
        ..., ge=0, le=100, example=12
    )

    Services_Subscribed: int = Field(
        ..., ge=0, le=10, example=5
    )

    Contract_Type: str = Field(
        ..., example="Month-to-Month"
    )

    MonthlyCharges: float = Field(
        ..., gt=0, example=70.5
    )

    TotalCharges: float = Field(
        ..., ge=0, example=500.75
    )

    TechSupport: str = Field(
        ..., example="Yes"
    )

    OnlineSecurity: str = Field(
        ..., example="Yes"
    )

    InternetService: str = Field(
        ..., example="Fiber optic"
    )


    @ field_validator('Gender')
    @classmethod
    def validate_gender(cls, value):
        allowed = {"Male","Female"}

        if value not in allowed:
            raise ValueError(f"Gender must be {allowed}")
        
        return value
    
    @classmethod
    @field_validator('Contract_type')
    def validation_contract_type(cls,value):
        allowed = {'Month-to-month',"One year","Two year"}

        if value not in allowed:
            raise ValueError(f"contractype must be {allowed}")
        
        return value



    @classmethod
    @field_validator('TechSupport')

    def validation_Tech_Support(cls,value):
        allowed = {"Yes","No"}

        if value not in allowed:
            raise ValueError(f"techsupport must be {allowed}")
        
        return value
    
    @classmethod
    @field_validator('InternetService')

    def validation_internet_service(cls, value):
        allowed = {'DSL','Fiber optic','No'}
        if value not in allowed:
            raise ValueError(f"internetservice must be {allowed}")
        
        return value


#Output Schema
class PredictionResponse(BaseModel):
    churn_prediction: int
    churn_label : str
    churn_probability : Optional[float]


#Predicton Endpoint
@app.post('/', response_model=PredictionResponse)
def predict(customer: CustomerData):
    try:
        input_df = pd.DataFrame([customer.model_dump()])

        prediction = model.predict(input_df)[0]

        probability = None
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(input_df)[0][1]

        return PredictionResponse(
            churn_prediction=prediction,
            churn_label="Churn" if prediction == 1 else "No churn",
            churn_probability=probability
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    








