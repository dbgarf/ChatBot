import pytest
from src import redis_client
import requests

class MockGoodResponse:
    @staticmethod
    def json():
        return {
            "abbreviation":"PDT",
            "client_ip":"67.166.33.116",
            "datetime":"2020-08-18T21:07:06.950048-07:00",
            "day_of_week":2,
            "day_of_year":231,
            "dst":True,
            "dst_from":"2020-03-08T10:00:00+00:00",
            "dst_offset":3600,
            "dst_until":"2020-11-01T09:00:00+00:00",
            "raw_offset":-28800,
            "timezone":"America/Los_Angeles",
            "unixtime":1597810026,
            "utc_datetime":"2020-08-19T04:07:06.950048+00:00",
            "utc_offset":"-07:00",
            "week_number":34
        }

class MockInvalidTimezoneResponse:
    @staticmethod
    def json():
        # heavily abridged list
        return [
            'America/Adak', 
            'America/Anchorage', 
            'America/Araguaina', 
            'America/Argentina/Buenos_Aires', 
            'America/Argentina/Catamarca', 
            'America/Argentina/Cordoba', 
            'America/Argentina/Jujuy', 
            'America/Argentina/La_Rioja'
        ]

class MockNotFoundResponse:
    @staticmethod
    def json():
        return {'error': 'unknown location'}


@pytest.fixture
def mock_good_response(monkeypatch):

    def mock_get(*args, **kwargs):
        r = MockGoodResponse()
        r.status_code = 200
        return r 

    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def mock_invalid_timezone_response(monkeypatch):

    def mock_get(*args, **kwargs):
        r = MockInvalidTimezoneResponse()
        r.status_code = 200
        return r 

    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def mock_not_found_response(monkeypatch):

    def mock_get(*args, **kwargs):
        r = MockNotFoundResponse()
        r.status_code = 404
        return r

    monkeypatch.setattr(requests, "get", mock_get)

class MockRedis:
    def __init__():
        self.data = {}

    def get(key):
        return self.data.get(key)

    def set(key, val):
        self.data[key] = val

@pytest.fixture
def mock_redis(monkeypatch):

    def mock_r():
        return MockRedis()

    monkeypatch.setattr(redis_client, "get_redis_client", mock_r)