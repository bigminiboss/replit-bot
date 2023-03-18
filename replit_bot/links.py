"""a few links"""

from os import environ


class links:
    """bot urls (docs)"""

    if (
        "REPL_SLUG" not in environ
        or "REPL_OWNER" not in environ
        or "REPLIT_DB_URL" not in environ
    ):
        docs: str = None
    else:
        docs: str = f"https://{environ['REPL_SLUG']}.{environ['REPL_OWNER']}.repl.co"
