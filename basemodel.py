import re
from pydantic import BaseModel


class Item(BaseModel):
    Id_items= int
    Description_items = str
    Quantity_items = int
    Mesure_items = str
    Cost_items = float
    Num_invoice = str

class SignInModel(BaseModel):
    email: str
    f: str

class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    admin: bool 