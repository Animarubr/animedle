from fastapi import APIRouter, Request
from animedle.controlers.check import CheckGuest

home = APIRouter()

@home.get("/")
async def root():
    return {"message": "only for tests"}

@home.post("/check")
async def check_guest(data: Request = None):
    if data:
        data = await data.json()
        result = CheckGuest()
        return result.handle_result(data["target"])

    