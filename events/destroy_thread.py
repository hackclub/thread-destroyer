from slack_sdk.web.async_client import AsyncWebClient
from utils.env import env
from utils.queue import add_message_to_delete_queue

async def destroy_thread(user_id: str, channel_id: str, root_ts: str, client: AsyncWebClient):
    await client.chat_postMessage(channel=channel_id, thread_ts=root_ts, text="This thread is being destroyed...")
    messages = await client.conversations_replies(
        channel=channel_id, ts=root_ts
    )
    for message in messages["messages"]:
        add_message_to_delete_queue(
            channel_id=channel_id, message_ts=message["ts"]
        )
    # send first message to logs
    await client.chat_postMessage(
        channel=env.slack_log_channel,
        text=f"Thread `{root_ts}` is being destroyed in <#{channel_id}> by <@{user_id}>.\nFirst message:\n```{messages['messages'][0]['text']}```",
    )