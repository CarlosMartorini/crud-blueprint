from flask import Flask
from app.views.animes_routes import bp_animes
# from app.views.anime_id import bp_anime_id

def init_app(app: Flask):

    app.register_blueprint(bp_animes)

    # app.register_blueprint(bp_anime_id)


# TODO: Limpar os comentários acima se realmente não for usar.
    