from fastapi import FastAPI
from datetime import datetime
import uvicorn

app = FastAPI(title="Time API", description="Simple test backend returning current server time")

@app.get("/")
async def get_server_time():
    """
    Returns the current server time in ISO 8601 format.
    """
    return {
        "server_time": datetime.now().isoformat()
    }

@app.get("/date")
async def get_server_date():
    """
    Returns the current server date in YYYY-MM-DD format.
    """
    return {
        "server_date": datetime.now().date().isoformat()
    }

if __name__ == "__main__":
    # You can run this directly with `python main.py` or via `uvicorn main:app --reload`
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
