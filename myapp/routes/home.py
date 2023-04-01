import base64
import pickle
import openai
import starlette.status as status
from fastapi import APIRouter, Request, Form 
from myapp.utils.utils import Utils
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

def register_home_path(app):
    templates.env.globals["url_path_for"] = app.url_path_for

@router.get("/")
def home(request: Request):
    cookie_value  = request.cookies.get("result")
    result = ""
    if cookie_value:
        result = pickle.loads(base64.b64decode(cookie_value.encode("utf-8")))
    
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@router.post("/")
def home(videoURL: str = Form()):
    comments = Utils.get_youtube_comments(videoURL)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= Utils.generate_prompt(comments),
        n=1,
        stop=None,
        max_tokens=2048,
        temperature=0.8,
    )
    redirect_response = RedirectResponse(
        url='/',
        status_code=status.HTTP_302_FOUND,
    )
    result = base64.b64encode(pickle.dumps(response.choices[0].text)).decode("utf-8")
    redirect_response.set_cookie("result", result)
    return redirect_response