from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:5173",  # Adjust this to your frontend's URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "ERP Chatbot backend is running"}
 