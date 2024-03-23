import uuid

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException

from slock.schemas import (
    GenerateClusterActionResponse,
    GetClusterActionResponse,
    GeneratedClusterActionRequest,
)

from slock.chains.cluster_action import generate_cluster_action_idea_chain, cluster_actions

cluster_action_router = APIRouter(prefix="/cluster_action")


@cluster_action_router.post(
    "/",
    summary="Generate a cluster action.",
    responses={
        201: {"description": "Successfully initiated task."},
    },
)
async def generate_cluster_action(
    r: GeneratedClusterActionRequest, background_tasks: BackgroundTasks
) -> GenerateClusterActionResponse:
    """Initiates a cluster action generation for you."""

    action_id = uuid.uuid4()
    background_tasks.add_task(
        generate_cluster_action_idea_chain,
        action_id,
        r.raw_message,
        r.span_id,
        r.timestamp,
    )
    return GenerateClusterActionResponse(id=action_id, completed=False)


@cluster_action_router.get(
    "/{id}",
    summary="Get the generated a cluster_action idea.",
    responses={
        200: {"description": "Successfully fetched cluster_action."},
        404: {"description": "cluster_action not found."},
    },
)
async def get_cluster_action(r: Request, id: uuid.UUID) -> GetClusterActionResponse:
    """Returns the cluster_action generation for you."""
    if id in cluster_actions:
        act = cluster_actions[id]
        return GetClusterActionResponse(
            id=act.id, completed=act.completed, action=act.action
        )
    raise HTTPException(status_code=404, detail="ID not found")