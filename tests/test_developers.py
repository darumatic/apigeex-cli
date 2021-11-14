from apigee.apiproducts.commands import delete
import json
import uuid
from click.testing import CliRunner
from apigee.developers.commands import (create, delete, get, list, set_status, 
                                        update, update_attr, delete_attr, get_attrs, 
                                        update_all_attrs)

runner = CliRunner()
test_dev = {
    "email": f"john.smith.{uuid.uuid4()}@email.com", 
    "firstName": "john", 
    "lastName": "smith", 
    "userName": "jsmith", 
    "attributes": [{"name": "env", "value": "test"}]
}

def test_create_developer():
    res = runner.invoke(
        create, 
        [
            "-e", test_dev["email"], 
            "--first-name", test_dev["firstName"], 
            "--last-name", test_dev["lastName"], 
            "--user-name", test_dev["userName"], 
            "--attributes", json.dumps({"attributes": test_dev["attributes"]})
        ]
    )
    assert res.output is not None and "error" not in res.output
    for val in test_dev.values():
        if isinstance(val, str):
            assert val in res.output
        else:
            json.dumps({"attributes": val}) in res.output

def test_get_developer():
    res = runner.invoke(get, ["-e", test_dev["email"]])
    assert res.output is not None and "error" not in res.output and test_dev["email"] in res.output and test_dev["userName"] in res.output

def test_list_developers():
    res = runner.invoke(list, ["--expand"])
    assert res.output is not None and "error" not in res.output and test_dev["email"] in res.output and test_dev["userName"] in res.output

def test_set_developer_status():
    res = runner.invoke(set_status, ["-e", test_dev["email"], "--action", "inactive"])
    assert res.output is not None and "error" not in res.output and "204" in res.output
    assert "inactive" in runner.invoke(get, ["-e", test_dev["email"]]).output
    
def test_get_all_attrs():
    res = runner.invoke(get_attrs, ["-e", test_dev["email"]])
    assert res.output is not None and "error" not in res.output and test_dev["attributes"][0]["name"] in res.output and test_dev["attributes"][0]["value"] in res.output

def test_update_developer():
    body = json.dumps({**test_dev, "userName": "jsmith02"})
    res = runner.invoke(update, ["-e", test_dev["email"], "-b", body])
    assert res.output is not None and "error" not in res.output and "jsmith02" in res.output

def test_update_developer_attr():
    res = runner.invoke(update_attr, ["-e", test_dev["email"], "--attribute-name", test_dev["attributes"][0]["name"], "--updated-value", "dev"])
    assert res.output is not None and "error" not in res.output and "dev" in res.output

def test_delete_developer_attr():
    res = runner.invoke(delete_attr, ["-e", test_dev["email"], "--attribute-name", test_dev["attributes"][0]["name"]])
    assert res.output is not None and "error" not in res.output and "env" in res.output
    assert "404" in runner.invoke(delete_attr, ["-e", test_dev["email"], "--attribute-name", test_dev["attributes"][0]["name"]]).output

def test_update_all_attrs():
    body = json.dumps({"attributes": [*test_dev["attributes"], {"name": "cli_test", "value": "true"}]})
    res = runner.invoke(update_all_attrs, ["-e", test_dev["email"], "-b", body])
    assert res.output is not None and "error" not in res.output and "cli_test" in res.output and "env" in res.output

def test_get_developer_by_app():
    pass

def test_delete_developer():
    res = runner.invoke(delete, ["-e", test_dev["email"]])
    assert res.output is not None and "error" not in res.output