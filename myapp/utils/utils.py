import os
import re 
import urllib.request, json

from fastapi import FastAPI
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles as StarletteStaticFiles
from starlette.templating import Jinja2Templates as StarletteJinja2Templates

class Utils():
    def getIdFromUrl(videoUrl: str):
        rgx = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*"
        videoId = re.search(rgx, videoUrl)
        if videoId is not None:
            return videoId.group(7)
        else:
            return None
        
    def get_youtube_comments(videoURL: str):
        videoId = Utils.getIdFromUrl(videoURL)
        url = "https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={0}&key={1}".format(videoId, os.getenv("YT_API_KEY"))
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
        prompt = "what is the general impression on the comments in this video?. Prompt the important points about the comments. At the end prompt the best and worst comment. Comments: ".join(comments)
        return prompt
    
    def setup_templates(app: FastAPI):
        templates = StarletteJinja2Templates(directory="templates")
        async def on_startup():
            # Register the url_path_for function globally for all templates
            templates.env.globals['url_path_for'] = app.url_path_for

        app.add_event_handler("startup", on_startup)
        app.mount("/static", StarletteStaticFiles(directory="static"), name="static")
        return templates