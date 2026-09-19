from hashlib import sha256
from threading import RLock
from flask import Flask, jsonify, request

app = Flask(__name__)

def leaf_hash(value):
    return sha256(("0:" + value).encode()).hexdigest()

def pair_hash(left, right):
    return sha256(("1:" + left + right).encode()).hexdigest()

class MerkleTree:
    def __init__(self):
        self.values = []
        self.lock = RLock()

    def add(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("value must be a non-empty string")
        with self.lock:
            self.values.append(value)

    def root(self):
        with self.lock:
            if not self.values:
                return None
            level = [leaf_hash(v) for v in self.values]
            while len(level) > 1:
                level = [pair_hash(level[i], level[i+1] if i+1 < len(level) else level[i])
                         for i in range(0, len(level), 2)]
            return level[0]

    def hashes(self):
        with self.lock:
            return [leaf_hash(v) for v in self.values]

    def verify(self, index, value):
        with self.lock:
            return (isinstance(index, int) and 0 <= index < len(self.values)
                    and isinstance(value, str) and self.values[index] == value)

    def clear(self):
        with self.lock:
            self.values.clear()

tree=MerkleTree()

@app.get("/health")
def health():
    return jsonify({"status":"ok","service":"merkle-tree"})

@app.post("/api/leaves")
def add():
    body=request.get_json(silent=True)
    if not isinstance(body,dict) or not isinstance(body.get("value"),str) or not body["value"]:
        return jsonify({"error":"non-empty string 'value' is required"}),400
    tree.add(body["value"])
    return jsonify({"added":True,"root":tree.root()}),201

@app.post("/api/leaves/batch")
def batch():
    body=request.get_json(silent=True)
    values=body.get("values") if isinstance(body,dict) else None
    if not isinstance(values,list) or not values or not all(isinstance(v,str) and v for v in values):
        return jsonify({"error":"non-empty string list 'values' is required"}),400
    for value in values: tree.add(value)
    return jsonify({"added":len(values),"root":tree.root()}),201

@app.get("/api/root")
def get_root():
    return jsonify({"root":tree.root(),"leaf_count":len(tree.values)})

@app.get("/api/leaves")
def leaves():
    return jsonify({"leaves":tree.hashes()})

@app.post("/api/verify")
def verify():
    body=request.get_json(silent=True)
    if not isinstance(body,dict) or not isinstance(body.get("index"),int) or not isinstance(body.get("value"),str):
        return jsonify({"error":"integer 'index' and string 'value' are required"}),400
    return jsonify({"valid":tree.verify(body["index"],body["value"]),"root":tree.root()})

@app.delete("/api/leaves")
def clear():
    tree.clear()
    return jsonify({"cleared":True,"root":None})

@app.get("/api/stats")
def stats():
    return jsonify({"leaf_count":len(tree.values),"root":tree.root()})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
