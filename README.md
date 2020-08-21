### scripted installation

1. clone the repo into the directory of your choice, this is the project directory
2. from the project directory, run the `install.sh`

### manual installation

1. clone the repo into the directory of your choice, this is the project directory
2. install redis-server, which is a depedency. this might vary based on your OS, but for a Debian-derived linux its just `sudo apt-get install redis-server`
3. from the project directory, initialize a virtualenv `virtualenv venv`
4. from the project directory, activate the virtualenv `source venv/bin/activate`
5. from the project directory, install python requirements with pip `pip install -r requirements.txt`

### running tests

from the project directory run `pytest`

additional documentation for pytest here: https://docs.pytest.org/en/stable/

### running the HTTP server

from the project directory run `uvicorn src.api:app`

you can now make requests to the chatbot server on `http://127.0.0.1:8000`

additional documentation for uvicorn here: https://www.uvicorn.org/

### making a request to the server

example of a timeat request: `http://127.0.0.1:8000?message=dan: !timeat America/Denver`

example of a timepopularity request: `http://127.0.0.1:8000?message=dan: !timepopularity America`

the querystring parameter `message` is required, and the server will return an error response if it's not present. 
