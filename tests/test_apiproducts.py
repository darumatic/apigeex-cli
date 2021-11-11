import json
import uuid
from click.testing import CliRunner
from apigee.apiproducts.commands import create

test_api_product = f"test-product-{uuid.uuid4()}"
def test_create_apiproduct():
    runner = CliRunner()
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
    assert res.exit_code == 0
    assert "201" in res.output
