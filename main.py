from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI()

# Конфигурация JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Роли и их разрешения
ROLES = {
    "admin": ["read", "write", "delete"],
    "user": ["read", "write"],
    "guest": ["read"]
}

# Пример данных пользователей
USERS_DATA = [
    {
        "username": "john_doe",
        "password": "securepassword123",
        "role": "admin"
    },
    {
        "username": "jane_doe",
        "password": "userpassword123",
        "role": "user"
    },
    {
        "username": "guest_user",
        "password": "guestpassword123",
        "role": "guest"
    }
]

class User(BaseModel):
    username: str
    password: str

def authenticate_user(username: str, password: str) -> dict:
    for user in USERS_DATA:
        if user["username"] == username and user["password"] == password:
            return {"username": user["username"], "role": user["role"]}
    return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return {"username": username, "role": role}

def has_permission(required_permission: str):
    async def check_permission(current_user: dict = Depends(get_current_user)):
        user_role = current_user["role"]
        if required_permission not in ROLES.get(user_role, []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user
    return check_permission

# Конечная точка для входа (POST)
@app.post("/login")
async def login(user: User):
    user_data = authenticate_user(user.username, user.password)
    if user_data:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data["username"], "role": user_data["role"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

# Защищенная конечная точка (GET)
@app.get("/protected_resource")
async def protected_resource(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! You have access to the protected resource."}

# Конечная точка для администратора (DELETE)
@app.delete("/admin/resource")
async def delete_resource(current_user: dict = Security(has_permission("delete"))):
    return {"message": "Resource deleted by admin"}

# Конечная точка для пользователя (PUT)
@app.put("/user/resource")
async def update_resource(current_user: dict = Security(has_permission("write"))):
    return {"message": "Resource updated by user"}

# Конечная точка для гостя (GET)
@app.get("/guest/resource")
async def read_resource(current_user: dict = Security(has_permission("read"))):
    return {"message": "Resource read by guest"}
