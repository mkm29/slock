import uuid
from datetime import datetime

from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from loguru import logger

from slock.schemas import ClusterAction

cluster_actions = {}


async def generate_cluster_action_cluster_action_chain(
    id: uuid.UUID, raw_message: str, span_id: str, timestamp: datetime
):
    logger.info(f"cluster action generation starting for {id}")
    # need to make this a self-hosted model
    chat = ChatOpenAI()
    system_template = """
    You are an AI Kubernetes agent that will help suggest, execute and measure corrective cluster actions.
    
    raw_message = {raw_message}.
    span_id = {span_id}.
    timestamp = {timestamp}
    """
    cluster_actions[id] = ClusterAction(id=id, completed=False, action="")

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{travel_request}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    request = chat_prompt.format_prompt(
        raw_message=raw_message,
        span_id=span_id,
        timestamp=timestamp,
    ).to_messages()
    result = chat(request)
    cluster_actions[id].cluster_action = result.content
    logger.info(f"Completed cluster_action generation for {id}")