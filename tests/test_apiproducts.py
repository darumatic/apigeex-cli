import json
import os
import uuid
from click.testing import CliRunner
from apigee.apiproducts.commands import create, delete, get, list, update, push
from apigee.utils import write_file

test_api_product = f"test-product-{uuid.uuid4()}"
runner = CliRunner()

def test_create_apiproduct():
    body = json.dumps(
        {
            "name":test_api_product, 
            "displayName":test_api_product, 
            "approvalType":"auto", 
            "attributes":
            [
                {"name":"access","value":"public"}
            ]
        }
    )
    res = runner.invoke(create, ["-n", test_api_product, "-b", body])
    assert res.output is not None and "error" not in res.output and test_api_product in res.output

def test_get_api_product():
    res = runner.invoke(get, ["-n", test_api_product])
    assert res.output is not None and "error" not in res.output and test_api_product in res.output

def test_list_api_products():
    res = runner.invoke(list)
    assert res.output is not None and "error" not in res.output and test_api_product in res.output

def test_update_api_products():
    body = json.dumps(
        {
            "name":test_api_product, 
            "displayName":test_api_product, 
            "approvalType":"manual", 
            "attributes":
            [
                {"name":"access","value":"public"}
            ]
        }
    )
    res = runner.invoke(update, ["-n", test_api_product, "-b", body])
    assert res.output is not None and "error" not in res.output and test_api_product in res.output and "manual" in res.output

def test_delete_apiproduct():
    res = runner.invoke(delete, ["-n", test_api_product])
    assert res.output is not None and "error" not in res.output and test_api_product in res.output

push_cmd_test_cases = {
    "create": {
        "name": "push_create",
        "displayName": "push_create",
        "approvalType": "manual",
        "attributes":
            [
                {"name":"access","value":"public"}
            ]
    },
    "update": {
        "name": "push_update",
        "displayName": "push_update",
        "approvalType": "auto"
    },
    "fail": {
        "name": "push_fail",
        "displayName": "push_fail",
        "attributes":
            [
                {"name":"access","value":"public"}
            ]
    }
}

def test_push_apiproduct_create():
    json_file = "./create.json"
    write_file(json.dumps(push_cmd_test_cases["create"]), json_file)
    res = runner.invoke(push, ["-f", json_file])
    assert res.output is not None and "error" not in res.output and "manual" in res.output and "attributes" in res.output
    os.remove(json_file)


def test_push_apiproduct_update():
    json_file = "./update.json"
    write_file(json.dumps(push_cmd_test_cases["update"]), json_file)
    res = runner.invoke(push, ["-f", json_file])
    assert res.output is not None and "error" not in res.output and "auto" in res.output and "attributes" not in res.output
    os.remove(json_file)

def test_push_apiproduct_fail():
    json_file = "./fail.json"
    write_file(json.dumps(push_cmd_test_cases["fail"]), json_file)
    res = runner.invoke(push, ["-f", json_file])
    assert res.output is not None and "error" in res.output
    os.remove(json_file)