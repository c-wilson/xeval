"""
This module includes the main entry point for this program and the main classes for the reputation service.

This encapsulates an abstract (portable) vision of the reputation service which can be ported to use with
different we frameworks, databases, etc.

This module is not dependant on its sub-modules, with the exception of algorithms. In other words, the API
for RepServer must be adherered to by sub-components and changing sub-components will not break the logic
of these resources.


Todo:
    * eager computation?

"""

import falcon
from falcon.media.validators import jsonschema
from xeval import exceptions, storage, algorithms
from wsgiref import simple_server
import argparse

# JSON schema for POST and GET. These enforce the syntax and value bounds at the input level.
# This is nice except that returned HTTP errors will be vague and might be hard to debug.
post_json_schema = {
    "properties": {
        "reputer": {"type": "string"},
        "reputee": {"type": "string"},
        "repute": {
            'type': 'object',
            'properties': {
                'rid': {'type': 'string'},
                'feature': {"enum": list(storage.FEATURES)},
                'value': {
                    'type': 'number',
                    'minimum': 0.,
                    'maximum': 10.,
                }
            }
        }
    }
}

get_json_schema = {
    'properties': {
        'reputee': {'type': 'string'}
    }
}


class ReptorResource:
    """
    Falcon application for reputation.
    """

    def __init__(self, ):
        self._reputation_service = Reptor()

    @jsonschema.validate(get_json_schema)
    def on_get(self, req:falcon.Request, resp:falcon.Response):
        """Handles GET requests"""
        try:
            rep_name = req.media['reputee']
            scores = self._reputation_service.calc_scores(rep_name)
            resp.status = falcon.HTTP_200  # This is the default status
            resp.media = scores  # this is a property that will serialize scores dictionary automatically.
        except exceptions.ReputeeNotFoundError:
            raise falcon.HTTPError(falcon.HTTP_422, 'Reputee not found.')

    @jsonschema.validate(post_json_schema)
    def on_post(self, req:falcon.Request, resp: falcon.Response):
        try:
            self._reputation_service.update(req.media)
            resp.status = falcon.HTTP_202
        except exceptions.RidDuplicateError:
            raise falcon.HTTPError(falcon.HTTP_422, 'Rejected due to duplicate identifier')


class Reptor:
    """
    This handles confidence generation and database interactions.

    THIS SEEMS unnecessary now, but if we wanted to scale this thing with higher-end algorithms, we'll
    need to implement a task queue, and this class will provide that interface.
    """

    def __init__(self):
        self._db = storage.SimpleStore()

    def calc_scores(self, reputee_name):
        """
        Calculates and returns current reputation using current report format. This result can be serialized
        to JSON.

        Return is formatted as Python nested dictionaries with the following spec:
            {
              'algorithm_1': {'score': score, 'confidence': confidence_value},
              'algorithm_2': {...}
            }

        :param reputee_name: name of reputee.
        :return dictionary that will serialize to JSON POST spec.
        """

        clarity_vals = self._db.get_rep_values(reputee_name, 'clarity')
        reach_vals = self._db.get_rep_values(reputee_name, 'reach')

        reach_result = algorithms.reach(reach_vals)
        clarity_result = algorithms.clarity(clarity_vals)
        clout_result = algorithms.clout(clarity_vals, reach_vals)

        def _pack(score_confidence_tuple):
            score, confidence = score_confidence_tuple
            return {'score': score, 'confidence': confidence}

        result_dict = {
            'reach': _pack(reach_result),
            'clarity': _pack(clarity_result),
            'clout': _pack(clout_result)
        }

        return result_dict

    def update(self, data: dict):
        """
        Adds data for a reputee in the database. Data must adhere to JSON schema.

        TODO: update/save reputation data

        :param data: data structure annotated in JSON schema.
        :return: None
        """

        self._db.add_transaction(data)


class RequireJSON(object):
    """
    middleware to enforce
    """

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


parser = argparse.ArgumentParser(
    'reptorServer',
    description="A RESTful reputation server we can all enjoy."
)

parser.add_argument('--address', type=str, default='localhost', help='IP address for server (default localhost)')
parser.add_argument('--port', type=int, default=8000, help='port for http server (default 8000)')


def main():
    args = parser.parse_args()
    app = falcon.API()
    repter_resource = ReptorResource()
    app.add_route('/reptor', repter_resource)
    httpd = simple_server.make_server(args.address, args.port, app)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
