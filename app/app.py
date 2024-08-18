from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="Your API Title",
    description="RAG API.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Health Check",
            "description": "Operations with health check endpoints."
        },
        {
            "name": "Query",
            "description": "Operations related to querying the vector store."
        },
        {
            "name": "Document Processing",
            "description": "Operations for processing and uploading documents."
        },
    ],
)
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "GKE App V0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
