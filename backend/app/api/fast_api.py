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
    "http://localhost:5174",
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


# Nouveaux endpoints
@app.get("/sets/recent")
async def get_recent_sets():
    return [
        {
            "set_num": "75192-1",
            "name": "Millennium Falcon",
            "year": 2017,
            "num_parts": 7541,
        },
        {"set_num": "10276-1", "name": "Colosseum", "year": 2020, "num_parts": 9036},
        {
            "set_num": "21058-1",
            "name": "Great Pyramid of Giza",
            "year": 2022,
            "num_parts": 1476,
        },
        {
            "set_num": "10497-1",
            "name": "Galaxy Explorer",
            "year": 2022,
            "num_parts": 1254,
        },
        {"set_num": "31203-1", "name": "World Map", "year": 2021, "num_parts": 11695},
        {
            "set_num": "42143-1",
            "name": "Ferrari Daytona SP3",
            "year": 2022,
            "num_parts": 3778,
        },
    ]


@app.get("/stats")
async def get_stats():
    return {"totalSets": 19847, "totalParts": 89436, "totalThemes": 687}
