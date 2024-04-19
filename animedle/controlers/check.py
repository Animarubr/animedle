from jikanpy import Jikan
import datetime


class CheckGuest():
    def __init__(self) -> None:
        self.jikan = Jikan()
        self.anime_of_the_day = "Super Cub"
    
    @staticmethod    
    def __handle_data_result(raw):
        return {
            "thumb": raw["data"][0]["images"]["jpg"]["image_url"],
            "episodes": raw["data"][0]["episodes"],
            "titles": raw["data"][0]["titles"],
            "compleated": raw["data"][0]["status"],
            "release": raw["data"][0]["aired"]["from"],
            "score": raw["data"][0]["score"],
            "studio": raw["data"][0]["studios"][0]["name"],
            "genre": raw["data"][0]["genres"][0]["name"],
            "themes": raw["data"][0]["themes"][0]["name"],
        }
        
    def handle_result(self, target):
        search_result = self.jikan.search('anime', target)
        data = self.__handle_data_result(search_result)
        search_result = self.jikan.search('anime', self.anime_of_the_day)
        be = self.__handle_data_result(search_result)        
        response = {
            "episodeCheck": {
                "isLessEpisodes": data["episodes"] < be["episodes"],
                "isHigherEpisodes": data["episodes"] > be["episodes"],
                "isEqualEpisodes": data["episodes"] == be["episodes"],
                "episodeGuest": data["episodes"],
            },
            "compleatedCheck": {
                "isCompleated": True if "Finished Airing" in be["compleated"] else False,
                "compleatedGuest": True if "Finished Airing" in data["compleated"] else False
            },
            "studioCheck": {
                "isSameStudio": data["studio"] == be["studio"],
                "studioGuest": data["studio"]
            },
            "genreCheck": {
                "isSameGenre": data["genre"] == be["genre"],
                "genreGuest": data["genre"]
            },
            "themesCheck": {
                "isSamethemes": data["themes"] == be["themes"],
                "themesGuest": data["themes"]
            },
            "releaseCheck": {
                "isLessRelease": datetime.datetime.strptime(data["release"], "%Y-%m-%dT%H:%M:%S%z") <  datetime.datetime.strptime(be["release"], "%Y-%m-%dT%H:%M:%S%z"),
                "isHigherRelease": datetime.datetime.strptime(data["release"], "%Y-%m-%dT%H:%M:%S%z") >  datetime.datetime.strptime(be["release"], "%Y-%m-%dT%H:%M:%S%z"),
                "isEqualRelease": datetime.datetime.strptime(data["release"], "%Y-%m-%dT%H:%M:%S%z") ==  datetime.datetime.strptime(be["release"], "%Y-%m-%dT%H:%M:%S%z"),
                "releaseGuest": datetime.datetime.strptime(data["release"], "%Y-%m-%dT%H:%M:%S%z").year
            },
            "scoreCheck": {
                "isLessScore": data["score"] < be["score"],
                "isHigherScore": data["score"] > be["score"],
                "isEqualScore": data["score"] == be["score"],
                "scoreGuest": data["score"]
            },
            "isRight": True if data["titles"][0]["title"] == be["titles"][0]["title"] else False
        }
        
        if response["isRight"]:
            response["image"] = be["thumb"]
        else:
            response["image"] = data["thumb"]
            
        return response
