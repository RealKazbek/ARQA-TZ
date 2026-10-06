from fastapi import FastAPI

app = FastAPI(title="Driver Shift Diary API", version="0.1.0")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
