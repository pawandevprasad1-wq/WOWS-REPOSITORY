import os
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Templates directory setup
templates = Jinja2Templates(directory="templates")

# MongoDB Connection details
MONGO_URI = "mongodb+srv://pawandevprasad1_db_user:123451234500@cluster0.acobnxp.mongodb.net/?appName=Cluster0"
DB_NAME = "WOW"
COLLECTION_NAME = "WOW"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def search_data(q: str = Query(..., min_length=1)):
    query = q.strip()
    if not query:
        return []
    
    # Case-insensitive regex search across multiple fields
    regex_query = {"$regex": query, "$options": "i"}
    db_filter = {
        "$or": [
            {"name": regex_query},
            {"location": regex_query},
            {"phone no.": regex_query},
            {"id": regex_query}
        ]
    }
    
    try:
        cursor = collection.find(db_filter, {"_id": 0})
        results = await cursor.to_list(length=100)
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
