from pydantic import BaseModel

class ContactForm(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    note: str
