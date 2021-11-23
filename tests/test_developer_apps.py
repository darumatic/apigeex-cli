import json
import uuid
from click.testing import CliRunner
from apigee.developer_apps.commands import create, get, delete, create_empty, list, create_creds
from apigee.apiproducts.commands import create as create_api_product, delete as delete_api_product
from apigee.developers.commands import create as create_developer, delete as delete_developer

runner = CliRunner()
test_dev = {
  "email": f"john.smith.{uuid.uuid4()}@email.com", 
  "firstName": "john", 
  "lastName": "smith", 
  "userName": "jsmith", 
  "attributes": [{"name": "env", "value": "test"}]
}

test_api_product = {
  "name":f"developer_app_integration_test_{uuid.uuid4()}", 
  "displayName":"developer_app_integration_test", 
  "approvalType":"auto", 
  "attributes": [
      {"name":"access","value":"public"}
    ]
  }

test_app = {
  "apiProducts": [
    test_api_product["name"]
  ],
  "appId": str(uuid.uuid4()),
  "appFamily": "developer_app_test",
  "attributes": [
    {
      "name": "env",
      "value": "test"
    }
  ],
  "callbackUrl": "google.com",
  "developerId": test_dev["email"],
  "keyExpiresIn": 1000,
  "name": f"developer_app_test_{uuid.uuid4()}",
  "status": "approved"
}

def test_create_developer_app():
    res = runner.invoke(create_api_product, ["-n", "developer_app_integration_test", "-b", json.dumps(test_api_product)])
    assert res.output is not None and "error" not in res.output and "developer_app_integration_test" in res.output

    res = runner.invoke(
        create_developer, 
        [
            "-e", test_dev["email"], 
            "--first-name", test_dev["firstName"], 
            "--last-name", test_dev["lastName"], 
            "--user-name", test_dev["userName"], 
            "--attributes", json.dumps({"attributes": test_dev["attributes"]})
        ]
    )
    assert res.output is not None and "error" not in res.output

    res = runner.invoke(create, ["-e", test_dev["email"], "-d", test_dev["email"], "-b", json.dumps(test_app)])
    assert res.output is not None and "error" not in res.output

def test_get_developer_app():
    res = runner.invoke(get, ["-n", test_app["name"], "-d", test_dev["email"]])
    assert res.output is not None
    assert  "violations" not in res.output
    assert test_app["name"] in res.output and test_api_product["name"] in res.output

def test_create_empty_app():
    res = runner.invoke(create_empty, ["-n", "test", "-d", test_dev["email"], "--display-name", "test"])
    assert res.output is not None
    assert "error" not in res.output
    assert "consumerKey" not in res.output and "consumerSecret" not in res.output

def test_list_developer_apps():
    res = runner.invoke(list, ["-d", test_dev["email"]])
    assert res.output is not None and "error" not in res.output and test_app["name"] in res.output

def test_create_creds():
    res = runner.invoke(create_creds, ["-n", "test", "-d", test_dev["email"]])
    assert res.output is not None and "error" not in res.output and "consumerKey" in res.output and "consumerSecret" in res.output

def test_create_creds_associate_apiproduct():
    res = runner.invoke(create_creds, ["-n", "test", "-d", test_dev["email"], "--products", test_api_product["name"]])
    assert res.output is not None and "error" not in res.output and "consumerKey" in res.output and "consumerSecret" in res.output and test_api_product["name"] in res.output
    runner.invoke(delete, ["-n", "test", "-d", test_dev["email"]])

def test_delete_developer_app():
    res = runner.invoke(delete, ["-n", test_app["name"], "-d", test_dev["email"]])
    assert res.output is not None
    assert "error" not in res.output
    res = runner.invoke(delete, ["-n", test_app["name"], "-d", test_dev["email"]])
    assert "404" in res.output
    runner.invoke(delete_api_product, ["-n", test_api_product["name"]])
    runner.invoke(delete_developer, ["-e", test_dev["email"]])