from betanin.api import torrent_client
from betanin.api.orm.models.remote import Remote
from betanin.api.rest.base import BaseResource
from betanin.api.rest.models import request as request_models
from betanin.api.rest.models import response as response_models
from betanin.api.rest.namespaces import settings_ns
from betanin.extensions import db
from flask import request

@settings_ns.route('/remotes')
class RemotesResources(BaseResource):
    @staticmethod
    @settings_ns.marshal_list_with(response_models.remote)
    def get():
        'get all remote configs'
        return Remote.query.all()

    @staticmethod
    @settings_ns.marshal_with(response_models.remote)
    def post():
        'creates a new remote'
        remote_type = request.args.get('type')
        empty_config = torrent_client.get_default_config(remote_type)
        remote = Remote(type=remote_type,
                        config=empty_config)
        db.session.add(remote)
        db.session.commit()
        return remote


@settings_ns.route('/remotes/<int:remote_id>/config')
class RemotesResources(BaseResource):
    @staticmethod
    def put(remote_id):
        'update a remotes config'
        remote = Remote.query.filter_by(id=remote_id).first_or_404()
        remote.config = request.get_json(silent=True)
        db.session.commit()


@settings_ns.route('/remotes/<int:remote_id>')
class RemotesResources(BaseResource):
    @staticmethod
    def delete(remote_id):
        'deletes a remote'
        remote = Remote.query.filter_by(id=remote_id).first_or_404()
        db.session.delete(remote)
        db.session.commit()