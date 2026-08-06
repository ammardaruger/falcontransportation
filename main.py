from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils.email_configs import send_contact_email
from models import ContactForm
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app/static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app/templates"))

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/old")
def home(request: Request):
    return templates.TemplateResponse("homeold.html", {"request": request})

# PDF content page
@app.get("/catalog")
def pdf_content(request: Request):
    return templates.TemplateResponse("pdfContent.html", {"request": request})

# Serve catalog.json
@app.get("/catalog.json")
def get_catalog():
    return FileResponse(os.path.join(BASE_DIR, "app/static/catalog.json"))

# Serve catalog.pdf
@app.get("/catalog.pdf")
def get_pdf():
    return FileResponse(os.path.join(BASE_DIR, "app/static/catalog.pdf"))

@app.post("/contact")
async def contact(form: ContactForm):
    contact_details = form.dict()
    response = await send_contact_email(
        user_name=contact_details['name'],
        user_email=contact_details['email'],
        user_message=contact_details['note']
    )
    return response

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
