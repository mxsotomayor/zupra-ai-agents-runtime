from fastapi import APIRouter, HTTPException, Query
from docker import from_env as docker_from_env
from app.clients.redis_client import redis_client
from app.routes.threads.schemas import NewThreadRequest
from app.clients.docker_client import docker_client
from app.routes.threads.services import ThreadsService

router = APIRouter()

route_prefix = "/threads"

service =  ThreadsService()

@router.post(route_prefix , tags=["Threads"])
def create_thread(new_tool: NewThreadRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        inserted =  service.create_thread({
            **new_tool.model_dump()
        })
        
        return {"id": str(inserted)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Threads"])
def list_thread():
    try:
        return service.get_threads()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix + "/{thread_id}/history", tags=["Threads"])
def get_thread_history(thread_id: str, offset: int = Query(default=0), limit: int = Query(default=10)):
    """
    Get container information by name.
    """
    container_id = redis_client.get(thread_id)
    if not container_id:
        raise HTTPException(status_code=404, detail="Container not found in Redis")
    
    container = docker_client.containers.get(container_id)
    return {
        "id": container.id,
        "name": container.name,
        "status": container.status,
        "image": container.image.tags,
    }
