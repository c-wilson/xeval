import falcon
from falcon import testing
import pytest
import uuid
import json
from xeval.main import app
import numpy as np


@pytest.fixture
def client():
    return testing.TestClient(app)


### POST TESTING ###

# reputee data for testing. Same data is used for testing reach and clarity.
REPUTATION_DATA = {
    'you': [0., 4.3, 6., 10., 10.],
    'another': [0., 4.3, 6., 10., 10., 2., 2., 1., 3.],
    'last': [1., 3.]
}


def test_clarity_posts(client: testing.TestClient):
    _post_tester(client, 'clarity')


def test_reach_posts(client: testing.TestClient):
    _post_tester(client, 'reach')


def _post_tester(client: testing.TestClient, feature_name):
    # TEST GOOD VALUES:
    for r_name, rep_values in REPUTATION_DATA.items():
        post_params = [_post_generator(x, feature_name, r_name) for x in rep_values]
        for p in post_params:
            print(json.dumps(p))
            response = client.simulate_post('/reptor', body=json.dumps(p))
            assert response.status == falcon.HTTP_ACCEPTED  # accepted

    # TEST BAD VALUES:
    bad_vals = [-1., 11.]
    bad_val_params = [_post_generator(x, feature_name, 'you') for x in bad_vals]
    for p in bad_val_params:
        response = client.simulate_post('/reptor', body=json.dumps(p))
        assert response.status == falcon.HTTP_BAD_REQUEST

    # TEST DEGENERATE RIDS:
    duplicate = post_params[0]
    response = client.simulate_post('/reptor', body=json.dumps(duplicate))
    assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY


def _post_generator(val: float, feature: str, reputee_name):
    a = {
        "reputer": "me",
        "reputee": reputee_name,
        "repute": {
            "rid": str(uuid.uuid4()),  # high entropy id source
            "feature": feature,
            "value": val
        }
    }
    return a


### GET TESTING ###

# these methods also check that expected values are recovered from the different features


EXPECTED_RESULT = {  # based on above fake data.
    'another': {
        'clarity': {'confidence': 1.0, 'score': 4.2555555555555555},
        'clout': {'confidence': 1.0, 'score': 0.42555555555555558},
        'reach': {'confidence': 1.0, 'score': 4.2555555555555555}
    },
    'last': {
        'clarity': {'confidence': 0.0, 'score': 2.0},
        'clout': {'confidence': 0.0, 'score': 0.0},
        'reach': {'confidence': 0.0, 'score': 2.0}
    },
    'you': {
        'clarity': {'confidence': 0.125, 'score': 6.0600000000000005},
        'clout': {'confidence': 0.125, 'score': 0.60600000000000009},
        'reach': {'confidence': 0.875, 'score': 6.0600000000000005}
    }
}


def test_clarity_result(client: testing.TestClient):
    _get_feature_tester(client, 'clarity')


def test_clout_result(client: testing.TestClient):
    _get_feature_tester(client, 'clout')


def test_reach_result(client: testing.TestClient):
    _get_feature_tester(client, 'reach')


def _get_feature_tester(client: testing.TestClient, feature_name):

    for name, by_feature in EXPECTED_RESULT.items():
        getdict = {'reputee': name}
        result = client.simulate_get('/reptor', body=json.dumps(getdict))
        j = result.json  # type: dict
        method_result = j[feature_name]
        for datatype in ('score', 'confidence'):
            val = method_result[datatype]
            assert np.isclose(EXPECTED_RESULT[name][feature_name][datatype], val)
