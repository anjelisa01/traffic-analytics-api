from pydantic import EmailStr,BaseModel,ConfigDict

class WebsiteBase(BaseModel):
    name:str
    domain:str


class WebsiteUpdate(BaseModel):
    name:str   | None = None 
    domain:str  | None = None 