from loguru import logger
import os
import sys

# DETECT VERCEL
IS_VERCEL = os.getenv("VERCEL") == "1"

if IS_VERCEL:
    # On Vercel, use /tmp or just log to stderr (which Vercel captures)
    # Using /tmp ensures no crash, but stderr is better for dashboard viewing.
    # We will simply NOT add a file sink on Vercel to save IO, 
    # relying on the default stderr sink loguru provides.
    pass 
else:
    # Local development: Log to file
    log_dir = os.path.join(os.path.dirname(__file__), "../../data/logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
        logger.add(f"{log_dir}/app.log", rotation="1 MB", retention="10 days", level="INFO")
    except Exception:
        # Fallback if permission issues locally
        pass

class Logger:
    def __init__(self, name="app"):
        self.logger = logger.bind(name=name)

    def log(self, message):
        self.logger.info(message)
