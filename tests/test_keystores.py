import uuid
from click.testing import CliRunner
from apigee.keystores.commands import create, delete, delete_alias, get_alias, get_all_certs, list, get, list_aliases, create_alias, get_cert


test_keystore = f"test-keystore-{uuid.uuid4()}"
test_alias = {
    "alias": f"test-alias-{uuid.uuid4()}",
    "keySize": 2048, 
    "sigAlg": "SHA256withRSA", 
    "certValidityInDays": 2, 
    "subject": "{\"commonName\":\"test\"}", 
    "alternativeNames": "[\"test2\"]"           
}

runner = CliRunner()

def test_create_keystore():
    res = runner.invoke(create, ["-n", test_keystore, "-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_keystore in res.output

def test_list_keystores():
    res = runner.invoke(list, ["-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_keystore in res.output

def test_get_keystores():
    res = runner.invoke(get, ["-n", test_keystore, "-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_keystore in res.output

def test_create_alias():
    res = runner.invoke(
        create_alias,
        [
            "-n", test_keystore, "-e", "eval", "-a", test_alias["alias"], "-k", test_alias["keySize"], 
            "--sig-alg", test_alias["sigAlg"], "-v", test_alias["certValidityInDays"], "-s", test_alias["subject"], 
            "--alternative-names", test_alias["alternativeNames"]
        ]
    )
    assert res.output is not None and "error" not in res.output 
    assert test_alias["alias"] in res.output and str(test_alias["keySize"]) in res.output

def test_get_alias():
    res = runner.invoke(get_alias, ["-n", test_keystore, "--alias-name", test_alias["alias"], "-e", "eval"])
    assert res.output is not None and "error" not in res.output 
    assert test_alias["alias"] in res.output and str(test_alias["keySize"]) in res.output

def test_list_aliases():
    res = runner.invoke(list_aliases, ["-n", test_keystore, "-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_alias["alias"] in res.output
    
def test_get_cert():
    res = runner.invoke(get_cert, ["-n", test_keystore, "-e", "eval", "-a", test_alias["alias"]])
    assert res.output is not None and "error" not in res.output 
    assert test_alias["alias"] in res.output and str(test_alias["keySize"]) in res.output

def test_delete_alias():
    res = runner.invoke(delete_alias, ["-n", test_keystore, "-e", "eval", "--alias-name", test_alias["alias"]])
    assert res.output is not None and "error" not in res.output
    assert test_alias["alias"] in res.output
    res = runner.invoke(delete_alias, ["-n", test_keystore, "-e", "eval", "--alias-name", test_alias["alias"]])
    assert res.output is not None and "error" in res.output and "404" in res.output

def test_delete_keystore():
    res = runner.invoke(delete, ["-n", test_keystore, "-e", "eval"])
    assert res.output is not None and "error" not in res.output and test_keystore in res.output
    res = runner.invoke(delete, ["-n", test_keystore, "-e", "eval"])
    assert res.output is not None and "error" in res.output and "404" in res.output