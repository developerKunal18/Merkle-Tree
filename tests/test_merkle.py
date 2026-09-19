import pytest
import app as m

@pytest.fixture()
def client():
    m.tree=m.MerkleTree()
    m.app.config["TESTING"]=True
    with m.app.test_client() as c:
        yield c

def test_empty_root():
    assert m.MerkleTree().root() is None

def test_root_changes():
    t=m.MerkleTree()
    t.add("A")
    first=t.root()
    t.add("B")
    assert t.root()!=first

def test_batch_and_verify(client):
    r=client.post("/api/leaves/batch",json={"values":["A","B","C"]})
    assert r.status_code==201
    assert r.get_json()["root"]
    r=client.post("/api/verify",json={"index":1,"value":"B"})
    assert r.get_json()["valid"] is True

def test_wrong_value(client):
    client.post("/api/leaves",json={"value":"A"})
    assert client.post("/api/verify",json={"index":0,"value":"X"}).get_json()["valid"] is False

def test_leaf_hashes(client):
    client.post("/api/leaves/batch",json={"values":["A","B"]})
    assert len(client.get("/api/leaves").get_json()["leaves"])==2

def test_invalid_batch(client):
    assert client.post("/api/leaves/batch",json={"values":[]}).status_code==400

def test_clear(client):
    client.post("/api/leaves",json={"value":"A"})
    client.delete("/api/leaves")
    assert client.get("/api/root").get_json()["root"] is None
