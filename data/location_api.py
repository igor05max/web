import flask
from . import db_session
from .location import Location
from flask import jsonify
from flask import make_response


blueprint = flask.Blueprint(
    'location_api',
    __name__,
    template_folder='templates'
)


# API для получения всех локаций
@blueprint.route('/api/location')
def get_location():
    db_sess = db_session.create_session()
    location = db_sess.query(Location).all()
    return jsonify(
        {
            'locations':
                [item.to_dict(only=('id', 'name', 'category', 'count_visits', 'city.name'))
                 for item in location]
        }
    )
