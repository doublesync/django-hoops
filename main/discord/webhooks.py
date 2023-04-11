from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_urls = {
    "upgrade": "https://discord.com/api/webhooks/1090756321013420092/jrt5PCcMu887pPCPpMEVl0FXfRcMh-2lgSlk6ZtdaiaTUQdVZOuKVor25yGbRETcDfx6",
    "creation": "https://discord.com/api/webhooks/1091784933854416966/1WOK3XYnnvOQG9VwapLqnrnN-l-rUvL0mdnP33lBv_iqY4mtZLoXWG6KMUTSLQuRwR-Q",
    "coupon": "https://discord.com/api/webhooks/1091785073084350534/dVlxbquMtag2yP-QXZcphYHeyZNKBR-O6CqnouB9yxozMKOrJi8WmutUz_vnKwDbX_Ov",
    "cash": "https://discord.com/api/webhooks/1093686733318672424/G6Dondhfu84ytVtB3vglQ8Lbol_LGdg7TDy0mlH-O5fPWL6LowcAYPE4_6NA2OzErttw",
    "trade": "https://discord.com/api/webhooks/1095495035899883630/RUOqYoUltS8niJUfh3TQyYcxwwwAHNVVGeVeyJccg9FDB7tlWOA0NzTsWDQz3-5SJYbU",
}

default_webhook_msg = "Webhook test message"


def send_webhook(url, title="", message=""):
    # Create the webhook
    webhook = DiscordWebhook(url=webhook_urls[url])
    # Create an embed
    webhook_embed = DiscordEmbed(title=title, description=message, color="03b2f8")
    webhook_embed.set_timestamp()
    webhook_embed.set_footer(text="Powered by hoopsim.com")
    # Add embed object to webhook
    webhook.add_embed(webhook_embed)
    # Send webhook
    webhook.execute()
