from time import sleep
from queue import Queue
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .env import env

client = WebClient(token=env.slack_user_token)

delete_queue = Queue()


def process_queue():
    while True:
        channel_id, message_ts = delete_queue.get()
        try:
            client.chat_delete(channel=channel_id, ts=message_ts, as_user=True)
        except SlackApiError as e:
            if e.response["error"] == "ratelimited":
                retry_after = int(e.response.headers.get("Retry-After", 1))
                print(f"Rate limited, retrying in {retry_after} seconds.")
                sleep(retry_after)
                delete_queue.put((channel_id, message_ts))
            else:
                print(f"Failed to delete message: {e.response['error']}")
        sleep(0.1)
        delete_queue.task_done()


def add_message_to_delete_queue(channel_id, message_ts):
    delete_queue.put((channel_id, message_ts))
