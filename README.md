# Amis Backend/Blockchain Engineer Test

## Introduction
This is a simple in memory blockchain demo. This implementation is based on Flask framework. It allows user to view the whole blockchain and create TXs as well. I have no previous blockchain development experience, only concepts. But I did my best.

## Specification
- Account based (not UTXO)
- Single node (no network/p2p)
- No signature or verification involved
- Straightforward hash (no nonce, no mining)
- Initially issue 100 coins to new account
- Create new block per 10 seconds

## Implementation Details
- Python 3.6.4 used
- Hash function : SHA256
- TXs hash : Merkle tree (Ref : https://github.com/Tierion/pymerkletools) (For some weird reason I can't install/import merkletools module properly so I copied the whole class to my code)
- Log file can be read through http://127.0.0.1:8000/log

## Setup
```
sudo pip install Flask
python server.py
```

## Usage
- Main page : http://127.0.0.1:8000/
- Dump log : http://127.0.0.1:8000/log

## Screenshot
