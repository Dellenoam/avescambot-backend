from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router

app = FastAPI()

# Main router with global prefix /auth
router = APIRouter(prefix="/api")

# Include subrouter to main router
router.include_router(auth_router)

# Include main router to app
app.include_router(router)

# CORS
# In a real case, it's recommended to specify allowed origins, methods, and headers instead of using "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
