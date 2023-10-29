from flask import Flask
from flask_restx import Api, Resource

from src.server.instance import server
from src.models.animes import anime

app, api = server.app, server.api

animes_db = [
    {'id': 1, 'title': 'Konosuba'},
    {'id': 2, 'title': 'Naruto'},
    {'id': 3, 'title': 'Yoshihiro Togashi'},
    {'id': 4, 'title': 'Koyoharu Gotouge'},
    {'id': 5, 'title': 'Yūki Tabata'},
    {'id': 6, 'title': 'Shinichirō Watanabe'}
]

@api.route('/animes')
class Animelist(Resource):
    @api.marshal_list_with(anime)
    def get(self):
        return animes_db

    # Adicionar
    @api.expect(anime, validate=True)
    @api.marshal_with(anime)
    def post(self):
        response = api.payload
        animes_db.append(response)
        return response, 200
    
@api.route('/animes/<int:id>')
class Anime(Resource):
    @api.doc(params={'id': 'O ID do anime'})
    @api.doc(description='Consultar anime por ID')
    def get(self, id):
        anime = next((anime for anime in animes_db if anime['id'] == id), None)
        if anime is not None:
            return anime
        return {'message': 'Anime não encontrado'}, 404

    @api.expect(anime, validate=True)
    @api.marshal_with(anime)
    @api.doc(description='Editar anime por ID')
    def put(self, id):
        for anime in animes_db:
            if anime['id'] == id:
                anime.update(api.payload)
                return anime
        return {'message': 'Anime não encontrado'}, 404

    @api.doc(params={'id': 'O ID do anime'})
    @api.doc(description='Delete an anime by ID')
    def delete(self, id):
        for anime in animes_db:
            if anime['id'] == id:
                animes_db.remove(anime)
                return {'message': 'Anime deletado'}
        return {'message': 'Anime não encontrado'}, 404