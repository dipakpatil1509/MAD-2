from flask_caching import Cache
from flask import current_app
cache = Cache(current_app)
current_app.app_context().push()
