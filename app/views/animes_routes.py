from flask import Blueprint, request, jsonify
from app.services.animes_services import Animes

bp_animes = Blueprint('animes', __name__, url_prefix='/api')

@bp_animes.route('/animes', methods=['GET', 'POST'])
def get_create():
    
    data = request.get_json()

    try:
        Animes.verify_keys(data)
        Animes.create_table()
        new_anime_info = Animes(
            anime = data['anime'],
            released_date = data['released_date'],
            seasons = data['seasons']
        )
    except KeyError as e:
        return {'msg': e}, 422