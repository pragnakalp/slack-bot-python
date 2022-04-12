import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
import requests
from slack.errors import SlackApiError

# This is slack token
SLACK_TOKEN = "<Your slack token>"
# This is signing secret you get from slack developer console.
SIGNING_SECRET = "<Your signing secret>"

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

# initialize web client with slack token.
client = slack.WebClient(token=SLACK_TOKEN)

# This function call when message detect.
@ slack_event_adapter.on('message')
def sl_message(payload):
    print(payload)
    event = payload.get('event', {})
    # check event has text or not.
    if event.get('text'):
        try:
            # we get channel id fron event.
            channel_id = event.get('channel')
            # we get user
            user_id = event.get('user')
            # we get actual text that user send.
            text = event.get('text')
            
            if text == "hi":
                client.chat_postMessage(channel=channel_id, text="Hello")

            if text == "image":
                try:
                    response = client.files_upload(
                        file='/home/pragnakalpdev23/mysite/slack_file_display/download (2).jpg',
                        channels=channel_id
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["ok"] is False
                    # str like 'invalid_auth', 'channel_not_found'
                    assert e.response["error"]
                    print(f"Got an error: {e.response['error']}")

            if text == "video":
                try:
                    response = client.files_upload(
                        file='/home/pragnakalpdev23/mysite/slack_file_display/sample-mp4-file-small.mp4',
                        channels=channel_id
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["ok"] is False
                    # str like 'invalid_auth', 'channel_not_found'
                    assert e.response["error"]
                    print(f"Got an error: {e.response['error']}")

            if text == "file":
                try:
                    response = client.files_upload(
                        file='/home/pragnakalpdev23/mysite/slack_file_display/sample.pdf',
                        # initial_comment='This space ship needs some repairs I think...',
                        channels=channel_id
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["ok"] is False
                    # str like 'invalid_auth', 'channel_not_found'
                    assert e.response["error"]
                    print(f"Got an error: {e.response['error']}")

            if text == "audio":
                try:
                    response = client.files_upload(
                        file='/home/pragnakalpdev23/mysite/slack_file_display/file_example_MP3_700KB.mp3',
                        # initial_comment='This space ship needs some repairs I think...',
                        channels=channel_id
                    )
                except SlackApiError as e:
                    # You will get a SlackApiError if "ok" is False
                    assert e.response["ok"] is False
                    # str like 'invalid_auth', 'channel_not_found'
                    assert e.response["error"]
                    print(f"Got an error: {e.response['error']}")

            if text == "img":
                message_to_send = {"channel": channel_id, "blocks":  [
                    {
                        "type": "image",
                        "image_url": "https://i1.wp.com/thetempest.co/wp-content/uploads/2017/08/The-wise-words-of-Michael-Scott-Imgur-2.jpg?w=1024&ssl=1",
                        "alt_text": "inspiration"
                    }
                ]}

            try:
                return client.chat_postMessage(**message_to_send)
            except:
                print("No hi found")

            if text == "radiobtn":
                message_to_send = {"channel": channel_id, "blocks": [
                    {
                        "type": "input",
                        "element": {
                                "type": "radio_buttons",
                                "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "*this is plain_text text*",
                                                        "emoji": True
                                            },
                                            "value": "value-0"
                                        },
                                    {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "*this is plain_text text*",
                                                        "emoji": True
                                            },
                                            "value": "value-1"
                                            },
                                    {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "*this is plain_text text*",
                                                        "emoji": True
                                            },
                                            "value": "value-2"
                                            }
                                ],
                            "action_id": "radio_buttons-action"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Label",
                            "emoji": True
                        }
                    }
                ]}

            try:
                return client.chat_postMessage(**message_to_send)
            except:
                print("No found")
        except:
            print("No text found-->")
    else:
        # here we are store files to server when user send in chat.
        try:
            img_name = payload['event']['files'][0]['name']
            print("img_name:-->", img_name)
            img_url = payload['event']['files'][0]['url_private']
            print("img_url:-->", img_url)
            user_n = payload['event']['files'][0]['user']
            print("user_n:-->", user_n)
            file_name = img_url.split('/')[-1]
            print("file_name:-->", file_name)
            try:
                json_path = requests.get(img_url)
            except:
                print("nnnn mm ")
            if user_n != "U034MD9UNEM":
                with open(file_name, "wb") as f:
                    f.write(json_path.content)
                # open(img_name, 'wb').write(json_path.content)
        except:
            print("not found 1-->>")


if __name__ == "__main__":
    app.run(debug=True)