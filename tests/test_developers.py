from apigee.apiproducts.commands import delete
import json
import uuid
from click.testing import CliRunner
from apigee.developers.commands import create, delete

runner = CliRunner()
test_dev = {
    "email": f"john.smith.{uuid.uuid4()}@email.com", 
    "first_name": "john", 
    "last_name": "smith", 
    "username": "jsmith", 
    "attributes": [{"name": "env", "value": "test"}]
}

def test_create_developer():
    res = runner.invoke(
        create, 
        [
            "-e", test_dev["email"], 
            "--first-name", test_dev["first_name"], 
            "--last-name", test_dev["last_name"], 
            "--user-name", test_dev["username"], 
            "--attributes", json.dumps({"attributes": test_dev["attributes"]})
        ]
    )
    assert res.output is not None and "error" not in res.output
    for val in test_dev.values():
        if isinstance(val, str):
            assert val in res.output
        else:
            json.dumps({"attributes": val}) in res.output

def test_delete_developer():
    res = runner.invoke(delete, ["-e", test_dev["email"]])
    assert res.output is not None and "error" not in res.output