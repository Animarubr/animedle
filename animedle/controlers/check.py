from jikanpy import Jikan
import datetime

from animedle.models.mongo import Mongo


class CheckGuest(Mongo):
    def __init__(self) -> None:
        super().__init__()
        self.jikan = Jikan()
    
    def get_anime_of_the_day(self):
        col = self.database.get_collection("daily")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        anime_day = col.find_one({"data": today})
        return anime_day
    
    @staticmethod    
    def __handle_data_result(raw):
        if raw["data"]:
            data = raw["data"][0]
            return {
                "thumb": data["images"]["jpg"]["image_url"],
                "episodes": data.get("episodes"),
                "titles": data.get("titles"),
                "compleated": data.get("status"),
                "release": data["aired"]["from"],
                "score": data.get("score"),
                "studio": data["studios"][0]["name"] if data["studios"] else None,
                "genre": data["genres"][0]["name"] if data["genres"] else None,
                "themes": data["themes"][0]["name"] if data["themes"] else None,
            }
            
        return []
        
    def handle_result(self, target):
        anime_day = self.get_anime_of_the_day()
        search_result = self.jikan.search('anime', target)
        data = self.__handle_data_result(search_result)
        search_result = self.jikan.search('anime', anime_day.get("name"))
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
            "isCorrect": True if data["titles"][0]["title"] == be["titles"][0]["title"] else False
        }
        
        if response["isCorrect"]:
            response["image"] = be["thumb"]
        else:
            response["image"] = data["thumb"]
        
        return response
