# django-hoops
A web-app for "hoops" (a basketball league) made with Django, Bootstrap &amp; Postgres.

**Environment variables go in a file called '.env' in th emain directory.**
```
# [DISCORD OAUTH2]
DISCORD_AUTH_URL = "get_your_own"
CLIENT_ID = "get_your_own"
CLIENT_SECRET = "get_your_own"
GRANT_TYPE = "authorization_code"
REDIRECT_URI = "http://localhost:8000/login/discord/redirect" 
SCOPE = "identify guilds"

# [DISCORD GUILDS]
HOOPS_GUILD_ID = "discord_server_id"

# [SECRET KEYS]
DJANGO_SECRET_KEY = "make_your_own"

# [OTHERS]
DEVELOPMENT_MODE = "True"
DATABASE_URL = "sqlite:///db.sqlite3"
DEBUG = "True"
MOTD = "MOTD: The Pittsburgh Force are the worst team in the league."
```
