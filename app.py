import os

import openai
from fastapi import FastAPI, requests, Depends, Request, Form 
from fastapi.staticfiles import StaticFiles
import urllib.request, json
import starlette.status as status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Register url_path_for function with Jinja2
    templates.env.globals["url_path_for"] = app.url_path_for
    openai.api_key = "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"

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
def home(videoURL: str = Form()):
    comments = get_youtube_comments(videoURL)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(comments),
        n=1,
        stop=None,
        max_tokens=2048,
        temperature=0.8,
    )
    return RedirectResponse(
        f"/result?result={response.choices[0].text}", 
        status_code=status.HTTP_302_FOUND)

@app.get("/result")
def show_result(request: Request, result: str):
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

def get_youtube_comments(videoURL):
    url = "https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={}&key=AIzaSyApSDd8sguN8fmkFfPguz98DQIKx4nZ7sg".format(videoURL)
    response = urllib.request.urlopen(url)
    if response.status == 200:
        data = response.read()
        dict = json.loads(data)
        text_display = []
        # Loop through the 'items' array and print the value of 'textDisplay' for each comment
        for item in dict['items']:
            text_display.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
        return text_display

    # If the request was not successful, return an error message
    return 'Error: Unable to retrieve data from API'

def generate_prompt(comments):
    prompt = "what is the general impression on the comments in this video?. Prompt the important points about the comments. Also prompt the best and worst comment on the next paragraph. Comments: " + " || ".join(comments)
    return prompt
