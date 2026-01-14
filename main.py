import time, logging, random, uuid
from fastapi import FastAPI, Request, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger

# 1. ENHANCED LOGGING (Structured JSON)
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s %(trace_id)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="ta9ss Pro API")

# 2. METRICS (Prometheus)
Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def add_observability(request: Request, call_next):
    # Simulate TRACING: Generate a unique ID for every request
    trace_id = str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.info("request_processed", extra={
        "trace_id": trace_id,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration": round(duration, 4)
    })
    response.headers["X-Trace-ID"] = trace_id
    return response

@app.get("/")
def read_root():
    return {"status": "Online", "version": "2.0", "message": "ta9ss Weather Service"}

@app.get("/weather/{city}")
def get_weather(city: str):
    # Simulation of a "Real" logic with randomness
    cities = ["tunis", "sfax", "sousse", "bizerte"]
    if city.lower() not in cities:
        logger.error(f"City {city} not found")
        raise HTTPException(status_code=404, detail="City not supported")
    
    return {
        "city": city,
        "temp": random.randint(15, 35),
        "humidity": f"{random.randint(40, 90)}%",
        "timestamp": time.time()
    }

# 3. HEALTH CHECK (Requirement for Kubernetes)
@app.get("/health")
def health_check():
    return {"status": "healthy"}