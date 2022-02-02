import json
import os
import uuid
from click.testing import CliRunner
from apigee.keyvaluemaps.commands import create, delete, list, get


test_map = f"test-map-{uuid.uuid4()}"
runner = CliRunner()

def test_create_kvmap():
    res = runner.invoke(create, ["-n", test_map, "-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_map in res.output

def test_list_kvmap():
    res = runner.invoke(list, ["-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_map in res.output

def test_delete_kvmap():
    res = runner.invoke(delete, ["-n", test_map, "-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_map in res.output
    res = runner.invoke(delete, ["-n", test_map, "-e", "eval"])
    assert res.output is not None and "error" in res.output and "404" in res.output