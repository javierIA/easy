from importlib.resources import path
import os
import re
from fastapi import FastAPI, Request, Form,File,UploadFile,Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from db.controllers.invoicesController import delete_invoice, get_invoices, getmaxInvoices, update_invoice
from db.controllers.itemsController import get_items, get_item, add_item, getmaxItems, update_item, delete_item
from db.controllers.pdfController import get_pdf_by_author,add_pdf
from db.controllers.usersController import get_user_by_username, get_users, get_user, add_user, getmaxUsers, is_admin, delete_user, update_user_password,update_user
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from auth.emailtools import welcome
from auth.auth import AuthHandler
import basemodel 
import shutil
import pydantic
from typing import List
import aiofiles
import datetime
from pathlib import Path
from a2wsgi import ASGIMiddleware

app=FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
app.add_middleware(GZipMiddleware)
auth_handler = AuthHandler()
users = []

templates=Jinja2Templates(directory="templates")

@app.middleware("http")
async def create_auth_header(request: Request,call_next):
    
    if ("Authorization" not in request.headers and "Authorization" in request.cookies ):
        access_token = request.cookies["Authorization"]
        
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer {access_token}".encode()
            )
        )
        #print(request.headers)


    response = await call_next(request)
    if response.status_code == 403:
        return RedirectResponse("/login",status_code=302)
    return response


@app.post("/SignIn")
async def SignIn(username: str = Form(), password: str = Form()):
    user = get_user(username)
    print(auth_handler.get_password_hash(password))
    if not user:
        return {"message": "User not found"}
    if (user.email_users != username):
        return {"status" : 401, "message": "Email id is not register"}
    if not auth_handler.verify_password(password, user.password_users):
        return {"status" : 401, "message": "Invalid password"}
    
    token = auth_handler.encode_token(user.email_users)
    response = RedirectResponse(url="/",status_code=302)
    response.set_cookie("Authorization", token,httponly=True,secure=False)
    return response

@app.post("/SignUp")
def SignUp(auth_details: basemodel.SignUpModel):
    if get_user(auth_details.email) or get_user_by_username(auth_details.username):
        return {"status" : 401, "message": "Email id is already register"}
    try:                                    
        hashed_password = auth_handler.get_password_hash(auth_details.password)
        user=add_user(auth_details.email, hashed_password, auth_details.admin, auth_details.username)
        #redirect to login page
        
        #welcome(auth_details.email,temp_password=auth_details.password)
    except Exception as e:
        return {"status" : 409, "message": "Account already exists","error":e.__str__()}
    return RedirectResponse(url="/login",status_code=302)

@app.post("/newuser")
def SignUp(username: str = Form(), password: str = Form(),email: str = Form(),admin: bool = Form()):
    if get_user(email) or get_user_by_username(username):
        return {"status" : 401, "message": "Email id is already register"}
    try:                                    
        hashed_password = auth_handler.get_password_hash(password)
        user=add_user(email, hashed_password, admin, username)
        #welcome(auth_details.email,temp_password=auth_details.password)
    except Exception as e:
        return {"status" : 409, "message": "Account already exists","error":e.__str__()}
    return  RedirectResponse(url="/login",status_code=302)


@app.get("/SignUp")
def SignUp( request: Request):
    return templates.TemplateResponse("SignUp.html",{"request":request})
@app.get("/SignOut")
def SignOut(request: Request):
    response = RedirectResponse(url="/login",status_code=302)
    response.delete_cookie("Authorization")
    return response   
@app.get("/ResetPassword")
def ResetPasswordView(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})
@app.post("/ResetPassword")
def ResetPassword(email: str = Form(),password: str = Form()):
    user = get_user(email)
    if (user.email_users != email):
        return {"status" : 401, "message": "Email id is not register"}
    hashed_password = auth_handler.get_password_hash(password)
    update_user_password(email, hashed_password)
    return {"status" : 200, "message": "Password reset successfully."}

@app.get("/",)
async def index(request:Request,username=Depends(auth_handler.auth_wrapper)):
    if not is_admin(username):
        return templates.TemplateResponse("public/index.html", {"request": request,"username":username})
    return templates.TemplateResponse("index.html",{"request":request,"username":username})



@app.get("/admin")
async def index(request:Request,username=Depends(auth_handler.auth_wrapper)):
    itemsmax=getmaxItems()
    invoicesmax=getmaxInvoices()
    usermax=getmaxUsers()
    if not is_admin(username):
        return templates.TemplateResponse("public/index.html", {"request": request,"username":username})
    return templates.TemplateResponse("admin.html",{"request":request,"username":username,"itemsmax":itemsmax,"invoicesmax":invoicesmax,"usermax":usermax})


@app.get("/login")
async def login(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request})    

@app.get("/upload")
async def upload(request:Request,username=Depends(auth_handler.auth_wrapper)):
    if not is_admin(username):
        return templates.TemplateResponse("public/upload.html", {"request": request,"username":username})
    return templates.TemplateResponse("upload.html",{"request":request,"username":username})


@app.get("/invoices")
async def invoices(request:Request,username=Depends(auth_handler.auth_wrapper)):
    return templates.TemplateResponse("invoicestable.html",{"request":request,"username":username,"invoices":get_invoices()})




@app.post("/upload")
async def upload_post(files: List[UploadFile] = File(...),username=Depends(auth_handler.auth_wrapper)):
    try:
        path=Path("pdfs"+"/"+username)
        
        #create folder if not exist
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
    
            
        for file in files:
            destination_file_path = "./pdfs/"+file.filename 
            if os.path.exists(destination_file_path):
                os.remove(destination_file_path)
            async with aiofiles.open(destination_file_path, 'wb') as out_file:
                while content := await file.read(1024):
                    await out_file.write(content) 
            #rename file whith username and date and move to pdfs with username folder
            
            #if path.exists(destination_file_path):
            shutil.move(destination_file_path, "./pdfs/"+username+"/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_"+file.filename)
        
            destination_file_path = "./pdfs/"+username+"/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_"+file.filename
            absolute_path = os.path.abspath(destination_file_path)
            add_pdf(username,absolute_path)
            
        return {"Result": "OK", "filenames": [file.filename for file in files]}
    except Exception as e:
        return {"Result": "Error", "message": e.__str__()}



@app.get("/api/items")
async def item(items:list[basemodel.Item]=None,username=Depends(auth_handler.auth_wrapper)):    #list[basemodel.Item]
    data=get_items()
    aux = jsonable_encoder(data)
    item=aux
    return item

@app.post("/api/items/update/{Id_items}",status_code=200)
async def update_items(Id_items:str,request: Request,username=Depends(auth_handler.auth_wrapper)):
    print(Id_items)
    data= await request.json()
    update_item(Id_items=Id_items,Description_items=data["Description_items"],Quantity_items=data["Quantity_items"],Mesure_items=data["Mesure_items"],Cost_items=data["Cost_items"],Num_invoice=data["Num_invoice"])
    return {"success":"Item updated successfully"}


@app.post("/api/items/delete/{Id_items}",status_code=200)
async def delete_items(Id_items:str,request: Request,username=Depends(auth_handler.auth_wrapper)):
    print(Id_items)
    delete_item(Id_items=Id_items)
    return {"success":"Item deleted successfully"}

@app.get("/items")
async def items(request:Request,username=Depends(auth_handler.auth_wrapper)):
    print(getmaxItems())
    return templates.TemplateResponse("itemstabla.html",{"request":request,"username":username,"items":get_items()})

@app.get("/api/invoices/",status_code=200)
async def invoices(request:Request,username=Depends(auth_handler.auth_wrapper)):
    data=get_invoices()
    aux = jsonable_encoder(data)
    invoices=aux
    return invoices

@app.post("/api/invoices/update/{Id_invoices}",status_code=200)
async def update_invoices(Id_invoices:str,request: Request,username=Depends(auth_handler.auth_wrapper)):
    data= await request.json()
    update_invoice(Num_invoices=Id_invoices,Date_invoices=data["Date_invoices"],Origin_invoices=data["Origin_invoices"],Total_invoices=data["Total_invoices"],RFC_clients=data["RFC_clients"])
    return {"success":"Invoice updated successfully"}

@app.post("/api/invoices/delete/{Id_invoices}",status_code=200)
async def delete_invoices(Id_invoices:str,request: Request,username=Depends(auth_handler.auth_wrapper)):
    print(Id_invoices)
    delete_invoice(Id_invoices=Id_invoices)
    return {"success":"Invoice deleted successfully"}


@app.get("/api/users",status_code=200)
async def users(request:Request,username=Depends(auth_handler.auth_wrapper)):
    data=get_users()
    aux=jsonable_encoder(data)
    users=aux
    return users

@app.post("/api/users/update/{Id_users}",status_code=200)
async def update_users(Id_users:str,request: Request,username=Depends(auth_handler.auth_wrapper)):
    data= await request.json()
    update_user(Id_users=Id_users,Name_users=data["Name_users"],Lastname_users=data["Lastname_users"],Email_users=data["Email_users"],Password_users=data["Password_users"],Role_users=data["Role_users"])
    return {"success":"User updated successfully"}    

@app.post("/api/users/delete/{email}",status_code=200)
async def delete_users(email:str,request: Request,username=Depends(auth_handler.auth_wrapper)):
    print(email)
    delete_user(email=email)
    return {"success":"User deleted successfully"}

@app.get("/api/pdfs",status_code=200)
async def pdf(username=Depends(auth_handler.auth_wrapper)):
    data=get_pdf_by_author(username)
    pdf=jsonable_encoder(data)
    return pdf

@app.get("/api/pdfs/{user}",status_code=200)
async def userpdf(user:str,username=Depends(auth_handler.auth_wrapper)):
    data=get_pdf_by_author(user)
    pdf=jsonable_encoder(data)
    return pdf


wsgi_app = ASGIMiddleware(app)
