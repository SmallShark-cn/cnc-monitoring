from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from UserManagement import user_login, change_password

app = FastAPI()

# 允许 Vue 前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体模型
class LoginData(BaseModel):
    username: str
    password: str

# 登录接口
@app.post("/api/login")
async def login(data: LoginData):
    if user_login(data.username, data.password):
        return {"success": True, "message": "登录成功"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


# 定义修改密码请求体模型
class ChangePasswordData(BaseModel):
    username: str
    old_password: str
    new_password: str

# 修改密码接口
@app.post("/api/change-password")
async def change_password_api(data: ChangePasswordData):
    result = change_password(data.username, data.old_password, data.new_password)
    if result['success']:
        return {"success": True, "message": "密码修改成功"}
    else:
        raise HTTPException(status_code=400, detail=result['message'])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
