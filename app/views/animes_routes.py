from flask import Blueprint, request, jsonify
from app.services.animes_services import Anime

bp_animes = Blueprint('animes', __name__, url_prefix='/api')

@bp_animes.post('/animes')
def get_create():
    
    data = request.get_json()

    try:
        
        Anime.create_table()
        
        Anime.verify_keys(data)
        
        Anime.if_exists(data['anime'])
        
        new_anime_info = Anime(
            anime = data['anime'],
            released_date = data['released_date'],
            seasons = data['seasons']
        )

        return jsonify(new_anime_info.add_new_anime()), 201

    except KeyError as e:

        return {'msg': e}, 422
    
    except:

        return {'msg': f'{new_anime_info} already exists!'}, 409


@bp_animes.get('/animes')
def show_all_animes():

    Anime.create_table()

    result = Anime.get_all_animes()

    return {'data': result}, 200


@bp_animes.get('/animes/<int:anime_id>')
def filter(anime_id: int):

    Anime.create_table()

    try:

        result = Anime.get_specific_anime(anime_id)

        return result
    
    except:

        return {'msg': f'Anime with id {anime_id} not found!'}, 404


@bp_animes.patch('/animes/<int:anime_id>')
def update(anime_id):
    ...