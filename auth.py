# JWT Authentication
from new import app,CustomerData,PredictionResponse,predict
from fastapi.security import HTTPBearer # it is used for security purpose
from pydantic import BaseModel


# Configurations
SECRET_KEY = "sample_key" # it will be changes in production
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# security scheme
security = HTTPBearer()



# User authentication models
class UserRegister(BaseModel):
    username : str
    password : str

class UserLogin(BaseModel):
    username : str
    password : str



# class created for token body
class TokenResponse(BaseModel):
    access_token : str
    token_type : str # token type is bearer
    expires_in : int

class AuthenicatedPredictionRequest(BaseModel):
    customer : CustomerData


# creating fake user data

fake_users_db = {
    "admin" : {
        'username' : 'parv',
        'password' : 'okaydone',
        'disabled' : False
    },
    'user1' : {
        'username' : 'user1',
        'password' : 'user1pass',
        'disabled' : False
    }
}
from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional
# JWT access token
def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):  # wehave used optinal for expire delta becuase usko optinal bananna hai
     #expired_delta -> it means token kitne der me expire hojayega

    # 1. we will create copy of data to avoid mutation
    to_encode = data.copy()

    # 2. we will check if expires_delta is provided otherwise we will make default expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: # creating default expiry time
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # 3. Data -> we will add expiration time
    to_encode.update({'exp' : expire})

    
    # 4. we will encode our copy data, secret key, algorithm
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)


    # 5. then return the encoded token
    return encoded_jwt

import jwt
from fastapi import HTTPException
def verify_token(token:str):
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    username: str = payload.get('sub')

    if username is None:
        raise HTTPException(status_code=401,detail="invalid token")
    return username



def authenticate_user(username:str,password:str):
    user = fake_users_db.get(username) # get is a dictionary method
    if not user or user['password'] != password:
        return None
    return user


# 1. endpoint for user register
@app.post('/register',response_model=TokenResponse)
async def register_user(user:UserRegister):
    if user.username in fake_users_db:
        raise HTTPException (status_code=400, detail="username already exist")
    
    # register user
    fake_users_db[user.username] = {
        'username' :user.username,
        'password' : user.password,
        'disabled' : False

    }
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub' : user.username},expires_delta=access_token_expires)

    return{
        'access_token' : access_token,
        "token_type" : 'Bearer',
        "expires_in" : ACCESS_TOKEN_EXPIRE_MINUTES * 60 # time will be in seconds       
    }


# 2. endpoint for user login
@app.post('/login',response_model=TokenResponse)
async def login_user(user:UserLogin):
    if authenticate_user(user.username,user.password) is None:
        raise HTTPException(status_code=401,detail="invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub' : user.username},expires_delta=access_token_expires)

    return{
        'access_token' : access_token,
        "token_type" : 'Bearer',
        "expires_in" : ACCESS_TOKEN_EXPIRE_MINUTES * 60 # time will be in seconds       
    }

    

# Prediction endpoint with JWT authentication
# 1. post endpoint
# 2. response model  
# 3. verify Token  
# 4.log the authorized user  
# 5. call the original prediction function  


from fastapi import Depends
@app.post('/predict/auth',response_model=PredictionResponse,dependencies=[Depends(security)])

# extracts the authorization header, checks is the format of bearer token


async def predict_auth(request: AuthenicatedPredictionRequest,credentials=Depends(security)):
    # 3. verify Token  
    username = verify_token(credentials.credentials)

    # 4.log the authorized user 
    print(f"User{username} accessed the prediction endpoint")

    # 5. call the original prediction function

    return predict(request.customer) #we are extracting the customer data from the function.


