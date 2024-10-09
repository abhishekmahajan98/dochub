from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from backend.utils import azure_utils as azure

app = FastAPI()

class UserQuery(BaseModel):
    query: str

# Dictionary to store conversation history for each user and thread
conversation_history: Dict[str, Dict[str, List[Dict[str, str]]]] = {}

@app.post("/chat/{user_id}/{thread_id}")
async def chat(user_id: str, thread_id: str, body: UserQuery = Body(...)):
    # Initialize conversation history for this user and thread if it doesn't exist
    if user_id not in conversation_history:
        conversation_history[user_id] = {}
    if thread_id not in conversation_history[user_id]:
        conversation_history[user_id][thread_id] = []

    # Get relevant context
    context = azure.get_relevant_context(body.query)

    # Generate response
    response = azure.generate_response(
        query=body.query,
        context=context,
        conversation_history=conversation_history[user_id][thread_id]
    )

    # Add the current message and response to the conversation history
    conversation_history[user_id][thread_id].append({"role": "user", "content": body.query})
    conversation_history[user_id][thread_id].append({"role": "assistant", "content": response})
    print(conversation_history[user_id][thread_id])
    return f"Message Received to thread id: {thread_id} for user: {user_id}. Response: {response}"