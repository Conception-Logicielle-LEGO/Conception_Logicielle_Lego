from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Instantiate the web service
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/endpoint_entrainement")
async def endpoint_entrainement():
    return "Yay l'API marche"
