import re
from fastapi import FastAPI, Request, Form,File,UploadFile,Depends,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from db.controllers.invoicesController import delete_invoice, get_invoices, update_invoice
from db.controllers.itemsController import get_items, get_item, add_item, update_item, delete_item
from db.controllers.usersController import get_users, get_user, add_user, update_user, delete_user, update_user_password
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from auth.auth import AuthHandler
import basemodel 
import shutil
from pydantic import BaseModel

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
    print(auth_details)
    try:
        hashed_password = auth_handler.get_password_hash(auth_details.password)
        user=add_user(auth_details.email, hashed_password, auth_details.admin, auth_details.username)
        
    except Exception as e:
        return {"status" : 409, "message": "Account already exists","error":e.__str__()}
    return {"status" : 200, "message": "Sign Up successfully." ,"user": user}

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
    return templates.TemplateResponse("index.html",{"request":request})


@app.get("/admin")
async def index(request:Request,username=Depends(auth_handler.auth_wrapper)):
    return templates.TemplateResponse("admin.html",{"request":request})
@app.get("/login")
async def login(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request})    

@app.get("/upload")
async def upload(request:Request,username=Depends(auth_handler.auth_wrapper)):
    return templates.TemplateResponse("upload.html",{"request":request})
@app.get("/invoices")
async def invoices(request:Request,username=Depends(auth_handler.auth_wrapper)):
    return templates.TemplateResponse("invoicestable.html",{"request":request})




@app.post("/upload")
async def upload_post(request:Request,files:list[UploadFile]=File(...)):
    path='static/pdf/'

    for pdf in files: 
        with open(pdf.filename,"wb") as fd:
            try: 
              if pdf.content_type=='application/pdf':
                fd.write(pdf.file.read())
                shutil.move(pdf.filename,path)
                fd.close()
              else:
                    return templates.TemplateResponse("upload.html",{"request":request,"error":"File is not a pdf"})
            except Exception as e:
                return request.Response({"error":e})
            request.Response({"success":"File uploaded successfully"})


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
    return templates.TemplateResponse("itemstabla.html",{"request":request})
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
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", log_level="info",reload=True)