# vr-su | vehicle routing

## Installing (Local)

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
