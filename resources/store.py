from flask_jwt_extended import jwt_optional, get_jwt_identity
from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with name "{}"  already exists.'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message: Án error ocurred while creating the store.'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}


class StoreList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        stores = [store.json() for store in StoreModel.find_all()]
        if user_id:
            return {'stores': stores}
        else:
            return {'stores': [store['name'] for store in stores]}