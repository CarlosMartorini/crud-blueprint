from logging import error
from flask import Flask, jsonify
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

        cur.execute(
            """
                INSERT INTO animes 
                    (anime, released_date, seasons)
                VALUES
                    (%s, %s, %s)
                RETURNING
                    id
            """
            (self.anime, self.released_date, self.seasons)
        )

        close_connection(conn, cur)

        return {
            "anime": self.anime,
            "released_date": self.realesed_date,
            "seasons": self.seasons
        }


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

        list_animes = [Anime(data).__dict__ for data in result]

        return {"data": list_animes}

    
    @staticmethod
    def get_specific_anime(anime_id):
        conn = open_connection()
        
        cur = conn.cursor()

        cur.execute(
            """
                SELECT * FROM animes WHERE id = (%s)
            """
            (id, )
        )

        result = cur.fetchone()

        close_connection(conn, cur)

        anime = Anime(result).__dict__

        return {"data": anime}


    @staticmethod
    def if_exists(anime):

        list_animes = Anime.get_all_animes()

        result = [element for element in list_animes if element['anime'] == anime.title()]

        if len(result) > 0:
            raise error
    

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
                    """
                    (data['anime'].title(), anime_id)
                )

            if key == 'released_date':

                cur.execute(
                    """
                        UPDATE animes SET released_date = %s WHERE id = %s
                    """
                    (data['released_date'], anime_id)
                )
            
            if key == 'seasons':

                cur.execute(
                    """
                        UPDATE animes SET seasons = %s WHERE id = %s
                    """
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
            """
            (anime_id, )
        )

        close_connection(conn, cur)

