from flask_restplus import Resource, reqparse
from ..models.location import MineLocation
from ..models.mines import MineIdentity

from app.extensions import jwt


class MineLocationResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', type=str)
    parser.add_argument('surname', type=str)

    @jwt.requires_roles(["mds-mine-view"])
    def get(self, mine_location_guid):
        mine_location = MineLocation.find_by_mine_location_guid(mine_location_guid)
        if mine_location:
            return mine_location.json()
        return {'message': 'Mine Location not found'}, 404


class MineLocationListResource(Resource):
    @jwt.requires_roles(["mds-mine-view"])
    def get(self):
        return {'mines': list(map(lambda x: x.json_by_location(), MineIdentity.query.all()))}
