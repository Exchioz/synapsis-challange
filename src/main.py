import re
import uvicorn
import psycopg
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from langchain_postgres.chat_message_histories import PostgresChatMessageHistory
from langchain_core.messages.utils import trim_messages
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI

from list_tools import tools
from config import Config
from schema import ChatRequest, ChatResponse

app = FastAPI()
logger = logging.getLogger("uvicorn")
config = Config()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = str(request.session_id)
    user_input = str(request.user_input)
    logger.info(f"Session {session_id}: {user_input}")

    tool_map = {tool.name: tool for tool in tools}

    with psycopg.connect(config.pgurl) as conn:
        # create table if not exists
        PostgresChatMessageHistory.create_tables(conn, "message_store")

        history = PostgresChatMessageHistory("message_store", session_id, sync_connection=conn)
        model = ChatOpenAI(
            base_url=config.openai_base_url,
            api_key=config.openai_api_key,
            model=config.openai_model
        )
        model_tools = model.bind_tools(tools)

        history.add_user_message(user_input)
        messages = history.get_messages()

        chat = trim_messages(
            messages,
            strategy="last",
            max_tokens=config.number_last_message,
            token_counter=len
        )

        response = model_tools.invoke(chat)

        if response.tool_calls:
            tool_messages = []
            for tool_call in response.tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args")
                tool_id = tool_call.get("id")
                tool_output = tool_map[tool_name].invoke(tool_args)
                logger.info(f"Tool {tool_name} called with args {tool_args}, output: {tool_output}")

                tool_messages.append(ToolMessage(content=tool_output, tool_call_id=tool_id))
            
            final_messages = messages + [response] + tool_messages
            response = model_tools.invoke(final_messages)

        cleaned_response = re.sub(r"<think>.*?<\/think>", "", response.content, flags=re.DOTALL).strip()
        history.add_ai_message(cleaned_response)
        logger.info(f"AI response: {cleaned_response}")

        return ChatResponse(session_id=session_id, ai_response=cleaned_response)


@app.exception_handler(psycopg.Error)
async def database_exception_handler(request: Request, exc: psycopg.Error):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Database error occurred", "details": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred", "details": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(app, host=config.host_app, port=config.port_app)
