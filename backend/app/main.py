from fastapi import FastAPI

app = FastAPI(title="Tiro Job Tracker")


@app.get("/health")
def health():
    return {"status": "ok"}
