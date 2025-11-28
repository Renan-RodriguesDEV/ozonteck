from fastapi import FastAPI

app = FastAPI(title="Ozoneteck API", version="1.0.0")

@app.get("/states")
def states():
    return 