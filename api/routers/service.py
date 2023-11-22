from fastapi import APIRouter


service_router = APIRouter(
    prefix="/service",
    tags=["service"]
)


@service_router.get("/restart")
def service_restart():
    return {'msg': 'ok'}