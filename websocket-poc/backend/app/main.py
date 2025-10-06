import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import redis.asyncio as aioredis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
connections: list[WebSocket] = []

# Redis configuration
REDIS_URL = "redis://redis:6379"
CHANNEL = "chat_channel"
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def redis_listener():
    """
    Listen for messages on Redis channel and broadcast to all connected WebSockets.
    """
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL)
    logger.info("Subscribed to Redis channel: %s", CHANNEL)

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"]
            logger.info("Redis message received: %s", data)

            disconnected = []
            for ws in connections:
                try:
                    await ws.send_text(data)
                except Exception as e:
                    logger.warning("Failed to send to WebSocket: %s", e)
                    disconnected.append(ws)
            for ws in disconnected:
                connections.remove(ws)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Redis listener task...")
    asyncio.create_task(redis_listener())


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    logger.info("WebSocket connected: %s", ws.client)
    connections.append(ws)

    try:
        while True:
            data = await ws.receive_text()
            logger.info("Received from WS: %s", data)

            # Push messages to Redis list for history
            await redis_client.rpush("chat_history", f"User: {data}")

            # Publish messages to Redis channel
            await redis_client.publish(CHANNEL, f"User: {data}")
            bot_msg = f"Bot: You said '{data}'"
            await redis_client.publish(CHANNEL, bot_msg)
            await redis_client.rpush("chat_history", bot_msg)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: %s", ws.client)
        connections.remove(ws)


@app.get("/history")
async def get_history():
    """
    Returns the last 50 chat messages
    """
    messages = await redis_client.lrange("chat_history", -50, -1)
    logger.info("Fetched chat history: %d messages", len(messages))
    return {"messages": messages}
