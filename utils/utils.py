import re 

class Utils():
    def getIdFromUrl(videoUrl: str):
        rgx = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*"
        videoId = re.search(rgx, videoUrl)
        if videoId is not None:
            return videoId.group(7)
        else:
            return None