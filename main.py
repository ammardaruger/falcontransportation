from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils.email_configs import send_contact_email
from models import ContactForm
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Home page

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/old")
def home(request: Request):
    return templates.TemplateResponse("homeold.html", {"request": request})

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
        "main:app",          # Replace "main" with the name of your Python file
        host="0.0.0.0",    # The IP address to run the server on
        port=8000,           # The port to run the server on
        reload=True          # Reloads the server automatically when you change the code
    )