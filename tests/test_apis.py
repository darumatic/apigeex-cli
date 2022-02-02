import json
import os
import uuid
from click.testing import CliRunner
from apigee.apis.commands import delete_revision

test_api_proxy = "hello-world" # change once command to create api proxy has been added
runner = CliRunner()

#def test_delete_api_revision():
#    res = runner.invoke(delete_revision, ["-n", test_api_proxy, "-r", "1"])
#    assert res.output is not None and "error" not in res.output and test_api_proxy in res.output