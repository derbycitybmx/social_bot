# social_bot
Slack bot that posts to all social accounts

# Development
## Local
Setup your .env file with two variables:
```
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
```

** Start the application locally **
```
hatch run env uvicorn src.social_bot.app:app --reloa
```

**Start an API Gateway**
```
ngrok http --domain=whippet-healthy-implicitly.ngrok-free.app 8000
```