import os

from flask_dance.contrib.google import make_google_blueprint

google_bp = make_google_blueprint(
    client_id=os.getenv('USAON_BENEFIT_TOOL_GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('USAON_BENEFIT_TOOL_GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],
)
