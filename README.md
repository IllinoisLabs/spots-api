# Spots API

_“Talk is cheap. Show me the code.” - Linus Torvalds_

## Getting Started (Locally)

1. Run `python3 -m pip install -r requirements.txt` to install necessary packages.
2. Acquire `.env` file from Admin (Davis / Siraj), place in app root.
3. Run `python3 main.py` to start the Flask server on [http://localhost:8000](http://localhost:8000).

### Tests
Run `pytest`

## API Interface
### Endpoints
```
GET /api/spots
POST /api/spots
GET /api/spots/:id
PUT /api/spots/:id
DELETE /api/spots/:id
```

### Spot Object
```
_id : String
name : String
description : String
```
