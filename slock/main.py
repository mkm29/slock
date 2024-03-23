from fastapi import FastAPI

from slock.routes.cluster_action import cluster_action_router

app = FastAPI()
app.include_router(cluster_action_router)