import os
import requests 

class WorldTimeAPI:
    DEFAULT_DOMAIN = 'http://worldtimeapi.org'

    def __init__(self):
        self.base_domain = os.getenv('TIME_API') or self.DEFAULT_DOMAIN

    def get_time_at_timezone(self, tz):
        """
        tz should be a valid timezone of the form :area/location[/:region]

        sample response:
        {
            "abbreviation":"PDT",
            "client_ip":"67.166.33.116",
            "datetime":"2020-08-18T21:07:06.950048-07:00",
            "day_of_week":2,
            "day_of_year":231,
            "dst":true,
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
        
        """
        url = "{base_domain}/api/timezone/{tz}".format(base_domain=self.base_domain, tz=tz)
        response = requests.get(url)

        if response.status_code == 200:
            return self.format_datetime(response.json().get('datetime'))

        if response.status_code == 404:
            return "Could not recognize timezone: %s" % tz

        if response.status_code == 500:
            return "Uh oh. Something's broken upstream. Try again later I guess."

        # fall through to this one if the server is doing something we haven't handled here
        # in a more robust environment would want to log this to a priority channel, cuz very unexpected
        return "World Time Service did something weird"

        def format_datetime(self, dt):
            "example of desired format: 9 Jun 2020 13:55"
            # I bet there's a python util in datetime module that will do what I want
            pass