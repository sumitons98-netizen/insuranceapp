# Insurance Webapp

A tiny Flask app with 5 fields (insured name, country, premium, limit, insured address),
shown on a web page and editable through a JSON API. Built to be deployed on Render and
updated later from a Python MCP server.

## Run locally

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

## API

Base URL = your app URL (locally `http://localhost:5000`, on Render `https://<your-app>.onrender.com`).

| Method     | Path           | Purpose                        |
|------------|----------------|--------------------------------|
| GET        | `/api/record`  | Read all 5 field values        |
| PUT / POST | `/api/record`  | Update one or more fields      |
| GET        | `/health`      | Health check                   |

Fields: `insured_name`, `country`, `premium`, `limit`, `insured_address`.

### Read

```bash
curl https://<your-app>.onrender.com/api/record
```

### Update (partial updates allowed)

```bash
curl -X PUT https://<your-app>.onrender.com/api/record \
  -H "Content-Type: application/json" \
  -d '{"insured_name": "Acme Corp", "country": "USA", "premium": "12000", "limit": "1000000", "insured_address": "1 Main St"}'
```

Response is the full updated record. The web page auto-refreshes every 3s, so updates
appear live.

## Deploy on Render

1. Push this folder to a GitHub repo.
2. Render Dashboard → New → Blueprint, pick the repo (uses `render.yaml`), **or**
   New → Web Service with:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
3. Your API base URL is the service URL Render gives you: `https://<your-app>.onrender.com`

> Note: Render's free filesystem is ephemeral — `data.json` resets on redeploy/restart.
> Fine for a demo. For durable storage, add a database.
