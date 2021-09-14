from flask import Flask, jsonify
from .db_services import open_connection, close_connection

class Animes:

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
            raise KeyError(keys)
            # TODO: importar e usar o InvalidKeysError(keys)
    

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

