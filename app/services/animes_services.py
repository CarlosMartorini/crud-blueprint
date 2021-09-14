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