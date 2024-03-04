from fastapi import FastAPI, APIRouter
from auth.routers import router as auth_router

app = FastAPI()

# Main router with global prefix /auth
router = APIRouter(prefix="/api")

# Include subrouter to main router
router.include_router(auth_router)

# Include main router to app
app.include_router(router)
