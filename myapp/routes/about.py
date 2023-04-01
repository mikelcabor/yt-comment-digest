from fastapi import APIRouter, Request 
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def register_about_path(app):
    templates.env.globals["url_path_for"] = app.url_path_for


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})