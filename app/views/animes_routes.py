from flask import Blueprint, request, jsonify
from app.services.animes_services import Anime
# from app.services.errors import InvalidKeyError

bp_animes = Blueprint('animes', __name__, url_prefix='/')

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

        result = new_anime_info.add_new_anime()

        return jsonify(result), 201

    except KeyError as e:

        return {'msg': e}, 422
    
    except:

        return {'msg': 'Anime already exists!'}, 409


@bp_animes.get('/animes')
def show_all_animes():

    Anime.create_table()

    result = Anime.get_all_animes()

    return jsonify({'data': result}), 200


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
    
    data = request.get_json()
    
    try:

        Anime.create_table()

        Anime.verify_keys(data)

        Anime.update(anime_id, data)

        return Anime.get_specific_anime(anime_id), 200

        # return result, 200

    except :

        return {'msg': f'Anime with id {anime_id} not founded!'}, 404


@bp_animes.delete('/animes/<int:anime_id>')
def delete(anime_id):
    
    try:

        Anime.create_table()

        Anime.delete(anime_id)

        return '', 204
    
    except:

        return {'msg': f'Anime with id {anime_id} not founded!'}, 404


