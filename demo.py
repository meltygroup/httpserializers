from httpserializers import serialize
from pathlib import Path
import requests

schema = requests.get("https://petstore3.swagger.io/api/v3/openapi.json").json()

# Supported content types:
# text/html
# application/json
# application/vnd.coreapi+json
# application/hal+json


content_type, response = serialize(
    {"id": 1, "name": "Jessica Right", "tag": "pet"},
    accept_header="text/html",
    hostname="127.0.0.1:5000",
    path="/pet/{petId}",
    schema=schema,
)

print(response)
