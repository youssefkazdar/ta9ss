import time, logging, random, uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger

# 1. ENHANCED LOGGING (Structured JSON)
logger = logging.getLogger()
logHandler = logging.StreamHandler()
# The trace_id will be added to every log line
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s %(trace_id)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="ta9ss Pro API")

# 2. METRICS (Prometheus) - Requirement: Observability
Instrumentator().instrument(app).expose(app)

# 3. FRONTEND MOUNTING - Requirement: Serving the Service
# This tells FastAPI that your HTML/CSS is in a folder called 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def add_observability(request: Request, call_next):
    # Requirement: TRACING - Unique ID for every request
    trace_id = str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    # Requirement: LOGS - Structured info about the request
    logger.info("request_processed", extra={
        "trace_id": trace_id,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration": round(duration, 4)
    })
    
    # Add the Trace ID to the browser header for debugging
    response.headers["X-Trace-ID"] = trace_id
    return response

@app.get("/")
async def read_index():
    # This serves your HTML file as the homepage
    return FileResponse('static/index.html')

@app.get("/weather/{city}")
def get_weather(city: str):
    # Requirement: REST API Logic
    cities = ["tunis", "sfax", "sousse", "bizerte", "kairouan"]
    if city.lower() not in cities:
        logger.error(f"City {city} not found")
        raise HTTPException(status_code=404, detail="City not supported")
    
    return {
        "city": city,
        "temp": random.randint(15, 35),
        "humidity": f"{random.randint(40, 90)}%",
        "timestamp": time.strftime("%H:%M:%S")
    }

# 4. HEALTH CHECK - Requirement: Kubernetes Probes
@app.get("/health")
def health_check():
    return {"status": "healthy"}