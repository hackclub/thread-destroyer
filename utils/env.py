from dotenv import load_dotenv
import os

load_dotenv()


class Environment:
    def __init__(self):
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        self.slack_user_token = os.environ.get("SLACK_USER_TOKEN")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
        self.slack_log_channel = os.environ.get("SLACK_LOG_CHANNEL")

        self.port = int(os.environ.get("PORT", 3000))

        if not self.slack_bot_token:
            raise Exception("SLACK_BOT_TOKEN is not set")
        if not self.slack_user_token:
            raise Exception("SLACK_USER_TOKEN is not set")
        if not self.slack_signing_secret:
            raise Exception("SLACK_SIGNING_SECRET is not set")
        if not self.slack_log_channel:
            raise Exception("SLACK_LOG_CHANNEL is not set")


env = Environment()
