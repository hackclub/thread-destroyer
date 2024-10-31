from slack_bolt.async_app import AsyncApp
from slack_sdk.web.async_client import AsyncWebClient
from .env import env
from events.destroy_thread import destroy_thread
from typing import Callable, Dict, Any

app = AsyncApp(token=env.slack_bot_token, signing_secret=env.slack_signing_secret)


@app.shortcut("destroy_thread")
async def handle_destroy_thread(
    ack: Callable[[], None], body: Dict[str, Any], client: AsyncWebClient
):
    await ack()
    channel_id = body["channel"]["id"]
    root_ts = body["message_ts"]
    user_id = body["user"]["id"]
    user = await client.users_info(user=user_id)
    if (
        user["user"]["is_admin"]
        or user["user"]["is_owner"]
        or user["user"]["is_primary_owner"]
    ):
        await client.views_open(
            user_id=user_id,
            view={
                "type": "modal",
                "callback_id": "destroy_thread",
                "title": {
                    "type": "plain_text",
                    "text": "Thread Destroyer",
                    "emoji": True,
                },
                "submit": {"type": "plain_text", "text": "DESTROY!", "emoji": True},
                "close": {"type": "plain_text", "text": "nowo v~v", "emoji": True},
                "blocks": [
                    {
                        "type": "section",
                        "block_id": f"{channel_id}-{root_ts}",
                        "text": {
                            "type": "mrkdwn",
                            "text": "You are about to permanently delete this thread. Are you sure you want to do this?\nThere is no going back.\nYou cannot undo this.",
                        },
                    }
                ],
            },
            trigger_id=body["trigger_id"],
        )
    else:
        await client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="You do not have permission to destroy threads.",
        )


@app.view("destroy_thread")
async def handle_destroy_thread_view(
    ack: Callable[[], None], body: Dict[str, Any], client: AsyncWebClient
):
    await ack()
    user_id = body["user"]["id"]
    channel_id, root_ts = body["view"]["blocks"][0]["block_id"].split("-")
    await destroy_thread(user_id, channel_id, root_ts, client)
