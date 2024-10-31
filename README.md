# Thread Destroyer

This is a really simple tool for admins to delete threads on Slack.

## Usage

- Clone this repository
- Create a Slack app (see example manifest below)
- Add a .env file (see `.env.example`)
- Create a virtual environment `python3 -m venv .venv`
- Activate the virtual environment `source .venv/bin/activate`
- Install the dependencies `python3 -m pip install -r requirements.txt`
- Run the script `python3 main.py`

```
{
    "display_information": {
        "name": "ThreadDestroyer"
    },
    "features": {
        "bot_user": {
            "display_name": "ThreadDestroyer",
            "always_online": false
        },
        "shortcuts": [
            {
                "name": "Destroy Thread",
                "type": "message",
                "callback_id": "destroy_thread",
                "description": "Delete this thread - There is no going back"
            }
        ]
    },
    "oauth_config": {
        "scopes": {
            "user": [
                "chat:write",
                "groups:history",
                "channels:history",
                "groups:write"
            ],
            "bot": [
                "channels:history",
                "groups:history",
                "chat:write",
                "channels:read",
                "groups:read",
                "users:read",
                "commands"
            ]
        }
    },
    "settings": {
        "interactivity": {
            "is_enabled": true,
            "request_url": "REQ_URL/slack/events"
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "token_rotation_enabled": false
    }
}
```