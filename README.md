# Merkle Tree

A Flask service demonstrating a Merkle Tree for efficient data-integrity verification.

## Features

- SHA-256 leaf hashing
- Pairwise parent hashing
- Merkle root calculation
- Batch insertion
- Leaf hash inspection
- Basic value verification
- Thread-safe operations
- Health and statistics endpoints
- Pytest test suite

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/leaves` | Add one value |
| POST | `/api/leaves/batch` | Add multiple values |
| GET | `/api/root` | Get Merkle root |
| GET | `/api/leaves` | Get leaf hashes |
| POST | `/api/verify` | Verify value at an index |
| DELETE | `/api/leaves` | Clear tree |
| GET | `/api/stats` | Tree statistics |

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Tests:

```bash
pytest -q
```

## Architecture

```text
             Merkle Root
                 |
          +------+------+
          |             |
       Hash AB        Hash CD
       /     \        /     \
    Hash A  Hash B  Hash C  Hash D
      |       |       |       |
    Data    Data    Data    Data
```

If any leaf changes, the resulting Merkle root changes.

## Learning Goals

Cryptographic hashing, tree structures, Merkle roots, data integrity, tamper detection, distributed synchronization, and blockchain fundamentals.
