import time
import logging
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger

# 1. Setup Structured Logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="ta9ss API")

# 2. Setup Metrics (Prometheus)
Instrumentator().instrument(app).expose(app)

# Mock Weather Data
weather_data = {
    "tunis": {"temp": 25, "condition": "Sunny"},
    "sfax": {"temp": 22, "condition": "Windy"},
    "kairouan": {"temp": 30, "condition": "Hot"}
}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info("request_processed", extra={
        "path": request.url.path,
        "method": request.method,
        "duration": duration,
        "status": response.status_code
    })
    return response

@app.get("/")
def read_root():
    return {"message": "Welcome to ta9ss Weather API"}

@app.get("/weather/{city}")
def get_weather(city: str):
    city = city.lower()
    if city in weather_data:
        return {"city": city, "data": weather_data[city]}
    return {"error": "City not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)