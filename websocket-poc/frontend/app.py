import os
import asyncio
import threading
import streamlit as st
import websockets
import logging

# ----------------- Logging Configuration -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ----------------- Streamlit Page Config -----------------
st.set_page_config(page_title="Real-time Chat", layout="wide")

# ----------------- Session State Initialization -----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "ws_connected" not in st.session_state:
    st.session_state["ws_connected"] = False

if "ws" not in st.session_state:
    st.session_state["ws"] = None

if "listener_started" not in st.session_state:
    st.session_state["listener_started"] = False

BACKEND_WS_URL = os.getenv("BACKEND_WS_URL_BROWSER", "ws://localhost:8000/ws")
placeholder = st.empty()

# ----------------- WebSocket Listener -----------------
async def listen_ws():
    """
    Persistent WebSocket listener.
    Receives messages from backend and updates chat UI in real-time.
    """
    try:
        async with websockets.connect(BACKEND_WS_URL) as ws:
            st.session_state["ws"] = ws
            st.session_state["ws_connected"] = True
            logger.info("Connected to backend WebSocket")

            while True:
                message = await ws.recv()
                logger.info("Message received from backend: %s", message)
                st.session_state["messages"].append(message)
                update_chat_ui()

    except Exception as e:
        st.session_state["ws_connected"] = False
        st.session_state["ws"] = None
        logger.error("WebSocket listener stopped: %s", e)
        await asyncio.sleep(5)  # Retry after 5 seconds
        await listen_ws()  # Reconnect automatically

def start_listener():
    """
    Runs the async WebSocket listener in a separate thread.
    """
    asyncio.run(listen_ws())

def update_chat_ui():
    """
    Renders all chat messages in Streamlit with color formatting.
    """
    with placeholder.container():
        for msg in st.session_state["messages"]:
            if msg.startswith("User:"):
                st.markdown(f"<div style='color: blue;'>{msg}</div>", unsafe_allow_html=True)
            elif msg.startswith("Bot:"):
                st.markdown(f"<div style='color: green;'>{msg}</div>", unsafe_allow_html=True)
            else:
                st.write(msg)

# ----------------- Start WebSocket Listener -----------------
if not st.session_state["listener_started"]:
    threading.Thread(target=start_listener, daemon=True).start()
    st.session_state["listener_started"] = True
    logger.info("WebSocket listener thread started")

# ----------------- Send Message -----------------
def send_message(msg_text: str):
    """
    Sends a message asynchronously via WebSocket without blocking Streamlit.
    """
    async def send_msg():
        try:
            ws = st.session_state.get("ws")
            if ws and st.session_state.get("ws_connected"):
                await ws.send(msg_text)
                logger.info("Sent message to backend: %s", msg_text)
        except Exception as e:
            logger.error("Failed to send message: %s", e)

    threading.Thread(target=lambda: asyncio.run(send_msg()), daemon=True).start()

# ----------------- Chat Input Form -----------------
with st.form("chat_form", clear_on_submit=True):
    msg = st.text_input("Type a message")
    submitted = st.form_submit_button("Send")

    if submitted and msg:
        # Append locally for instant UI update
        st.session_state["messages"].append(f"User: {msg}")
        logger.info("User typed message: %s", msg)
        send_message(msg)
        update_chat_ui()
