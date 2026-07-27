from fastapi import FastAPI

app = FastAPI(title="RAG MT Evaluator")

@app.get("/")
def root():
    return {"message": "Welcome to RAG MT Evaluator"}