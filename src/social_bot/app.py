from dotenv import load_dotenv
import json
import logging
import os
from typing import Dict, List
from fastapi import FastAPI, Request, Response, Body
from fastapi.responses import HTMLResponse
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import tweepy
load_dotenv()

"""
Status:
  - Slack channel setup
  - Channel workflow to post message setup
  - Slack App created and joined to the channel
  - uvicorn server running locally  
  - app deployed locally
  - app proxy setup and running locally on ngrok
  - app url updated
  - app tested and receiving message from slack

Next Steps:
  - ensure scaffold functionality of the app works
  - deconstruct message
"""
class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.environ.get("TWITTER_API_KEY"),
            consumer_secret=os.environ.get("TWITTER_API_SECRET"),
            access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
        )

    def post_tweet(self, text: str, media_urls: List[str] = None) -> None:
        # TODO: Implement media upload for Twitter
        self.client.create_tweet(text=text)

class FacebookClient:
    def __init__(self):
        # TODO: Implement Facebook API client
        pass

    def post_to_facebook(self, text: str, media_urls: List[str] = None) -> None:
        # TODO: Implement Facebook posting
        print(f"Posting to Facebook: {text}")

class InstagramClient:
    def __init__(self):
        # TODO: Implement Instagram API client
        pass

    def post_to_instagram(self, text: str, media_urls: List[str] = None) -> None:
        # TODO: Implement Instagram posting
        print(f"Posting to Instagram: {text}")

class SocialMediaHandler:
    def __init__(self):
        # self.twitter_client = TwitterClient()
        self.facebook_client = FacebookClient()
        self.instagram_client = InstagramClient()

    def post_to_all_platforms(self, text: str, media_urls: List[str] = None) -> None:
        # self.twitter_client.post_tweet(text, media_urls)
        self.facebook_client.post_to_facebook(text, media_urls)
        self.instagram_client.post_to_instagram(text, media_urls)

class SlackEventHandler:
    def __init__(self, social_media_handler: SocialMediaHandler):
        self.social_media_handler = social_media_handler

    def handle_channel_message(self, event: Dict, say: callable) -> None:
        print(f"Handling channel message: {event}")

        try:
            text = event['text']
            # media_urls = self.extract_media_urls(event)
            # self.social_media_handler.post_to_all_platforms(text, media_urls)
            # say("Successfully posted to all social media platforms!")
        except Exception as e:
            print(f"Error posting to social media: {e}")
            # say("Error posting to social media.")

    @staticmethod
    def extract_media_urls(event: Dict) -> List[str]:
        # TODO: Implement media URL extraction from Slack event
        return []

class SocialBotApp:
    def __init__(self):
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        slack_bot_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

        self.app = FastAPI()
        self.social_media_handler = SocialMediaHandler()
        self.slack_app = App(
            token=slack_bot_token,
            signing_secret=slack_bot_signing_secret
        )
        self.slack_event_handler = SlackEventHandler(self.social_media_handler)
        self.setup_routes()
        self.slack_app.event("message")(self.slack_event_handler.handle_channel_message)

    def setup_routes(self):
        slack_request_handler = SlackRequestHandler(self.slack_app)

        @self.app.post("/slack/events")
        async def slack_events(request: Request):
            body = await request.json()
            if body.get("type") == "url_verification":
                return {"challenge": body["challenge"]}

            try:
                result = await slack_request_handler.handle(request)
                print(f"Handler result: {result}")
                return result
            except Exception as e:
                print(f"Error processing Slack event: {e}")
                return {"error": str(e)}

        @self.app.get("/")
        async def root():
            return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Social Bot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            .container {
                text-align: center;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            p {
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Social Bot</h1>
            <p>Your Slack-to-Social Media integration is up and running!</p>
        </div>
    </body>
    </html>
    """, status_code=200)

    def run(self):
        import uvicorn
        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8000)),
            reload=True
        )


social_bot = SocialBotApp()
app = social_bot.app