# vrp-su | vehicle routing

A solver for the capacitated vehicle routing problem using ortools and fastapi.

* Vehicles do not need to return back to any depot since they carry infinite stock.    

* Vehicles have limited amount of stock.

* Jobs have predefined service durations.

## Usage

* `GET http://127.0.0.1:8000/` returns response code 200 if server is up and running.

* `POST http://127.0.0.1:8000/` expects a json body. returns response code 200 when a solution found. 500 otherwise (total demand at all locations exceeds the total capacity of the vehicles, no solution is possible).
  

Documentation to the webservice is also available at `/docs` (http://127.0.0.1:8000/docs or http://127.0.0.1:80/docs)

Job's service duration option can be turned off by setting `USE_SERVICE_TIME=False` environment variable or using an `.env` file.

### Installing (with Docker)

```
docker build -t routing .
docker run -d --name routing -p 80:80 routing

# run the server passing the configurations as environment variables
docker run -d --name routing -p 80:80 --env USE_SERVICE_TIME=False routing

```

### Installing (Local)

```
# Install and activate an virtual env (optional)
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate
```

```
# Install required python packages.
pip install -r requirements.txt

# run the server with
uvicorn routing.api:app --reload
```


## Development Setup

```
# Install and activate an virtual env (optional)
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate
```

```
# Install required python packages
pip install -r requirements.dev.txt

# run unit tests (optional)
pytest tests -s

# run the server with
uvicorn routing.api:app --reload

```

## 
