from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import prisma
from routers import user, category, transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000", # For React Next and Vue Domain that allow
    "http://localhost:5173" # Vite   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # * meaning allows all methods and headers to access
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(category.router)
app.include_router(transaction.router)