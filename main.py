from fastapi import FastAPI, HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
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

@app.get("/convert")
async def convert_time(utc_time: str, target_tz: str):
    """
    Converts a given UTC time string to a specified timezone.
    Parameters:
    - utc_time: UTC time in ISO 8601 format (e.g., '2026-03-16T12:00:00Z' or '2026-03-16T12:00:00+00:00')
    - target_tz: Target timezone name (e.g., 'Europe/Moscow', 'America/New_York')
    """
    try:
        # Replace 'Z' with explicit UTC offset for `fromisoformat` compatibility in some edge cases
        if utc_time.endswith('Z'):
            utc_time = utc_time[:-1] + '+00:00'
        
        dt_utc = datetime.fromisoformat(utc_time)
        
        # Ensure the datetime object behaves as UTC
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
        else:
            dt_utc = dt_utc.astimezone(ZoneInfo("UTC"))
            
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid UTC time format. Please provide a valid ISO 8601 string."
        )
        
    try:
        # Resolve target timezone
        tz = ZoneInfo(target_tz)
    except ZoneInfoNotFoundError:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid target timezone: '{target_tz}'. Please use standard IANA timezone names."
        )
        
    # Convert UTC to target timezone
    converted_dt = dt_utc.astimezone(tz)
    
    return {
        "original_utc_time": dt_utc.isoformat(),
        "target_timezone": target_tz,
        "converted_time": converted_dt.isoformat()
    }

if __name__ == "__main__":
    # You can run this directly with `python main.py` or via `uvicorn main:app --reload`
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
