from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from UserManagement import user_login, change_password, user_register, get_all_users, create_user, delete_user

router = APIRouter()

# 定义请求体模型
class LoginData(BaseModel):
    username: str
    password: str

class RegisterData(BaseModel):
    username: str
    password: str
    phone: str = None
    user_group: str = "普通用户"

class CreateUserData(BaseModel):
    username: str
    password: str
    phone: str = None
    user_group: str = "普通用户"

@router.post("/api/login")
async def login(data: LoginData):
    if user_login(data.username, data.password):
        return {"success": True, "message": "登录成功"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@router.post("/api/register")
async def register(data: RegisterData):
    result = user_register(data.username, data.password, data.phone, data.user_group)
    if result['success']:
        return {"success": True, "message": "注册成功"}
    else:
        raise HTTPException(status_code=400, detail=result['message'])

class ChangePasswordData(BaseModel):
    username: str
    old_password: str
    new_password: str

@router.post("/api/change-password")
async def change_password_api(data: ChangePasswordData):
    result = change_password(data.username, data.old_password, data.new_password)
    if result['success']:
        return {"success": True, "message": "密码修改成功"}
    else:
        raise HTTPException(status_code=400, detail=result['message'])

@router.get("/api/users")
async def get_users():
    result = get_all_users()
    if result['success']:
        return {"success": True, "users": result['users']}
    else:
        raise HTTPException(status_code=500, detail=result['message'])

@router.post("/api/users")
async def create_user_api(data: CreateUserData):
    result = create_user(data.username, data.password, data.phone, data.user_group)
    if result['success']:
        return {"success": True, "message": "用户创建成功"}
    else:
        raise HTTPException(status_code=400, detail=result['message'])

@router.delete("/api/users/{user_id}")
async def delete_user_api(user_id: int):
    result = delete_user(user_id)
    if result['success']:
        return {"success": True, "message": "用户删除成功"}
    else:
        raise HTTPException(status_code=400, detail=result['message'])
