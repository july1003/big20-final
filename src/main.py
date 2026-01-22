from fastapi import FastAPI

app = FastAPI(title="AI Mock Interview System")

@app.get("/")
def read_root():
    return {"message": "AI Mock Interview System is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
