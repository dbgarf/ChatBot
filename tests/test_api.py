from fastapi.testclient import TestClient

from src.api import app
from src.redis_client import get_redis_client

client = TestClient(app)

class TestChatBotAPI:
    def setup(self):
        r = get_redis_client()
        r.flushall()

    def test_message_is_required_querystring(self):
        response = client.get("/")
        assert response.status_code == 422
        response_content = response.json()['detail'][0]
        assert response_content['loc'] == ['query', 'message']
        assert response_content['msg'] == 'field required'
        assert response_content['type'] == 'value_error.missing'

    def test_valid_timeat_message(self, mock_good_response):
        url = "/?message=dan: !timeat America/Los_Angeles"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == '18 Aug 2020 21:07'

    def test_invalid_timeat_message(self, mock_not_found_response):
        url = "/?message=dan: !timeat Nowhere"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == "Unknown Timezone"

    def test_timepopularity_message(self, mock_good_response):
        # first do a timeat to increment the counter
        url ="/?message=dan: !timeat America/Los_Angeles"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == '18 Aug 2020 21:07'

        # then do a time popularity to get the count
        url = "/?message=dan: !timepopularity America/Los_Angeles"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == 1

        # then again...
        url ="/?message=dan: !timeat America/Los_Angeles"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == '18 Aug 2020 21:07'

        # ...and expect the count to be 2
        url = "/?message=dan: !timepopularity America/Los_Angeles"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == 2
    
    def test_undefined_command(self):
        url = "/?message=dan: !timewarp 1985"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == "undefined command. available commands: ['!timeat', '!timepopularity']"