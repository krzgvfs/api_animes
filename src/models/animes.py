from flask_restx import fields

from src.server.instance import server 

anime = server.api.model('Anime',{
    'id': fields.String(description='O ID do Registro'),
    'title': fields.String(required="True", min_length=1, max_lenght=300, description='O titulo do anime')
})