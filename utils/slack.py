from slack_bolt.async_app import AsyncApp
from slack_sdk.web.async_client import AsyncWebClient
from .env import env
from events.destroy_thread import destroy_thread
from typing import Callable, Dict, Any

app = AsyncApp(token=env.slack_bot_token, signing_secret=env.slack_signing_secret)

@app.shortcut("destroy_thread")
async def handle_destroy_thread(ack: Callable[[], None], body: Dict[str, Any], client: AsyncWebClient):
    await ack()
    channel_id = body["channel"]["id"]
    root_ts = body["message_ts"]
    user_id = body["user"]["id"]
    user = await client.users_info(user=user_id)
    if user["user"]["is_admin"] or user["user"]["is_owner"] or user["user"]["is_primary_owner"]:
        await destroy_thread(user_id, channel_id, root_ts, client)
    else:
        await client.chat_postEphemeral(channel=channel_id, user=user_id, text="You do not have permission to destroy threads.")