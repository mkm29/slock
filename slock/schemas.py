from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

class GenerateClusterActionResponse(BaseModel):
    id: uuid.UUID = Field(description="ID of the generated cluster action")
    completed: bool = Field(description="Flag indicating if the cluster action was taken")

class GetClusterActionResponse(GenerateClusterActionResponse):
    action: str = Field(description="The generated cluster action")

class GeneratedClusterActionRequest(BaseModel):
    raw_message: str = Field(description="The raw Kubernetes log")
    span_id: int = Field(description = "The eBPF ID corresponding to the parent span")
    timestamp: datetime = Field("The timestamp for the event")

class ClusterAction(GenerateClusterActionResponse):
    action: str = Field(description="The cluster action")