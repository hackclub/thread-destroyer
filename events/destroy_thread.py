from slack_sdk.web.async_client import AsyncWebClient
from utils.env import env
from utils.queue import add_message_to_delete_queue


async def destroy_thread(
    user_id: str, channel_id: str, root_ts: str, client: AsyncWebClient
):
    await client.chat_postMessage(
        channel=channel_id, thread_ts=root_ts, text="This thread is being destroyed..."
    )
    messages = await client.conversations_replies(channel=channel_id, ts=root_ts)
    message_log = []
    for message in messages["messages"]:
        m_user_id = message.get("user", "Unknown user")
        message_log.append(
            f"{m_user_id}: {message.get('text', 'There was no text associated with this message')}"
        )
        add_message_to_delete_queue(channel_id=channel_id, message_ts=message["ts"])

    message_log = "\n".join(message_log)

    log_msg = await client.chat_postMessage(
        channel=env.slack_log_channel,
        text=f"Thread `{root_ts}` has been destroyed in <#{channel_id}> by <@{user_id}>.\nFirst message:\n```{messages['messages'][0]['text']}```",
    )

    await client.files_upload_v2(
        channel=env.slack_log_channel,
        thread_ts=log_msg["ts"],
        content=message_log,
        initial_comment="Message log for the destroyed thread",
    )
