from logging import error

from flask.json import jsonify
from .db_services import open_connection, close_connection
from .errors import InvalidKeyError


class Anime:

    def __init__(self, anime, released_date, seasons):
        self.anime = anime.title()
        self.released_date = released_date
        self.seasons = seasons

    
    @staticmethod
    def create_table():
        
        conn = open_connection()

        cur = conn.cursor()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS animes (
                    id BIGSERIAL PRIMARY KEY,
                    anime VARCHAR(100) NOT NULL UNIQUE,
                    released_date DATE NOT NULL,
                    seasons INTEGER NOT NULL
                )
            """
        )

        close_connection(conn, cur)

    
    @staticmethod
    def verify_keys(data):

        needed_keys = ['anime', 'released_date', 'seasons']
        
        data_keys = data.keys()
        
        keys = [key for key in data_keys if key not in needed_keys]

        if len(keys) > 0:
            raise InvalidKeyError
    

    def add_new_anime(self):

        conn = open_connection()

        cur = conn.cursor()

        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """

        params = (self.anime, self.released_date, self.seasons)

        cur.execute(query, params)

        close_connection(conn, cur)

        return {
            "anime": self.anime,
            "released_date": self.released_date,
            "seasons": self.seasons
        }

        # TODO: acrescentar o id no retorno


    @staticmethod
    def get_all_animes():
        
        conn = open_connection()
        
        cur = conn.cursor()

        cur.execute(
            """
                SELECT * FROM animes
            """
        )

        result = cur.fetchall()

        close_connection(conn, cur)

        keys = ["id", "anime", "released_date", "seasons"]

        result_dict = [dict(zip(keys, row)) for row in result]

        return result_dict

    
    @staticmethod
    def get_specific_anime(anime_id):
        conn = open_connection()
        
        cur = conn.cursor()

        cur.execute(
            """
                SELECT * FROM animes WHERE id = (%s)
            """,
            (anime_id, )
        )

        result = cur.fetchall()

        close_connection(conn, cur)

        keys = ["id", "anime", "released_date", "seasons"]

        result_dict = [dict(zip(keys, row)) for row in result]

        return jsonify(result_dict)


    @staticmethod
    def if_exists(anime):

        list_animes = Anime.get_all_animes()

        result = [element for element in list_animes if element['anime'] == anime.title()]

        if len(result) > 0:
            return {'msg': 'This anime already exists!'}, 409
    

    @staticmethod
    def update(anime_id, data):

        conn = open_connection()

        cur = conn.cursor()

        keys = data.keys()

        # TODO: verificar se o id não vai dar erro

        for key in keys:

            if key == 'anime':

                cur.execute(
                    """
                        UPDATE animes SET anime = %s WHERE id = %s
                    """,
                    (data['anime'].title(), anime_id)
                )

            if key == 'released_date':

                cur.execute(
                    """
                        UPDATE animes SET released_date = %s WHERE id = %s
                    """,
                    (data['released_date'], anime_id)
                )
            
            if key == 'seasons':

                cur.execute(
                    """
                        UPDATE animes SET seasons = %s WHERE id = %s
                    """,
                    (data['seasons'], anime_id)
                )
        
        close_connection(conn, cur)


    @staticmethod
    def delete(anime_id):

        conn = open_connection()

        cur = conn.cursor()

        cur.execute(
            """
                DELETE FROM animes WHERE id = (%s) RETURNING *
            """,
            (anime_id, )
        )

        close_connection(conn, cur)

