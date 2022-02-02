import uuid
from click.testing import CliRunner
from apigee.references.commands import create, delete, list, get, update
from apigee.keystores.commands import create as create_keystore, delete as delete_keystore

test_keystore = f"test-keystore-{uuid.uuid4()}"
test_reference = {
    "name": f"test-ref-{uuid.uuid4()}",
    "description": "test",
    "resourceType": "KeyStore",
    "refers": test_keystore
}

runner = CliRunner()

def test_create_reference():
    runner.invoke(create_keystore, ["-n", test_keystore, "-e", "eval"])
    res = runner.invoke(
        create, 
        [
            "-n", test_reference["name"], "-e", "eval", "-d", test_reference["description"], 
            "-t", test_reference["resourceType"], "-r", test_reference["refers"]
        ]
    )
    assert res.output is not None and "error" not in res.output
    assert test_keystore in res.output and test_reference["name"] in res.output

def test_get_reference():
    res = runner.invoke(get, ["-n", test_reference["name"], "-e", "eval"])
    assert res.output is not None and "error" not in res.output
    assert test_keystore in res.output and test_reference["name"] in res.output and test_reference["description"] in res.output and test_reference["resourceType"] in res.output

def test_list_references():
    res = runner.invoke(list, ["-e", "eval"])
    assert res.output is not None and "error" not in res.output
    assert test_reference["name"] in res.output

def test_update_reference():
    updated_desc = "description after updating reference"
    res = runner.invoke(
        update, 
        [
            "-n", test_reference["name"], "-e", "eval", "-d", updated_desc, 
            "-t", test_reference["resourceType"], "-r", test_reference["refers"]
        ]
    )
    assert res.output is not None and "error" not in res.output
    assert test_keystore in res.output and test_reference["name"] in res.output and updated_desc in res.output

def test_delete_reference():
    res = runner.invoke(delete, ["-n", test_reference["name"], "-e", "eval"])
    assert res.output is not None and "error" not in res.output
    assert test_keystore in res.output and test_reference["name"] in res.output
    res = runner.invoke(delete, ["-n", test_reference["name"], "-e", "eval"])
    assert res.output is not None and "error" in res.output and "404" in res.output
    runner.invoke(delete_keystore, ["-n", test_keystore, "-e", "eval"])
