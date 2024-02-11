from . import app
from .views import add_movie, get_one_movie, get_movies
from app.auth.auth import signup, login, refresh, add_role

# movies route
app.add_url_rule('/movies', view_func=get_movies)
app.add_url_rule('/movies/<id>', view_func=get_one_movie)
app.add_url_rule('/movies', view_func=add_movie, methods=['POST'])

# auth routes
app.add_url_rule('/auth/login', view_func=login, methods=['POST'])
app.add_url_rule('/auth/signup', view_func=signup, methods=['POST'])
app.add_url_rule('/auth/refresh_token', view_func=refresh, methods=['POST'])
app.add_url_rule('/auth/roles/<id>', view_func=add_role, methods=['POST'])


