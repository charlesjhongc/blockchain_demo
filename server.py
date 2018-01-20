from flask import Flask, render_template, request, redirect, Response
import hashlib
import time
import threading

class MerkleTools(object):
    """Merkle Tree Tool"""
    def __init__(self, hash_type="sha256"):
        hash_type = hash_type.lower()
        if hash_type in ['sha256', 'md5', 'sha224', 'sha384', 'sha512',
                         'sha3_256', 'sha3_224', 'sha3_384', 'sha3_512']:
            self.hash_function = getattr(hashlib, hash_type)
        else:
            raise Exception('`hash_type` {} nor supported'.format(hash_type))

        self.reset_tree()

    def _to_hex(self, x):
        try:  # python3
            return x.hex()
        except:  # python2
            return binascii.hexlify(x)

    def reset_tree(self):
        self.leaves = list()
        self.levels = None
        self.is_ready = False

    def add_leaf(self, values, do_hash=False):
        self.is_ready = False
        # check if single leaf
        if not isinstance(values, tuple) and not isinstance(values, list):
            values = [values]
        for v in values:
            if do_hash:
                v = v.encode('utf-8')
                v = self.hash_function(v).hexdigest()
            v = bytearray.fromhex(v)
            self.leaves.append(v)

    def get_leaf(self, index):
        return self._to_hex(self.leaves[index])

    def get_leaf_count(self):
        return len(self.leaves)

    def get_tree_ready_state(self):
        return self.is_ready

    def _calculate_next_level(self):
        solo_leave = None
        N = len(self.levels[0])  # number of leaves on the level
        if N % 2 == 1:  # if odd number of leaves on the level
            solo_leave = self.levels[0][-1]
            N -= 1

        new_level = []
        for l, r in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):
            new_level.append(self.hash_function(l+r).digest())
        if solo_leave is not None:
            new_level.append(solo_leave)
        self.levels = [new_level, ] + self.levels  # prepend new level

    def make_tree(self):
        self.is_ready = False
        if self.get_leaf_count() > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self._calculate_next_level()
        self.is_ready = True

    def get_merkle_root(self):
        if self.is_ready:
            if self.levels is not None:
                return self._to_hex(self.levels[0][0])
            else:
                return None
        else:
            return None

    def get_proof(self, index):
        if self.levels is None:
            return None
        elif not self.is_ready or index > len(self.leaves)-1 or index < 0:
            return None
        else:
            proof = []
            for x in range(len(self.levels) - 1, 0, -1):
                level_len = len(self.levels[x])
                if (index == level_len - 1) and (level_len % 2 == 1):  # skip if this is an odd end node
                    index = int(index / 2.)
                    continue
                is_right_node = index % 2
                sibling_index = index - 1 if is_right_node else index + 1
                sibling_pos = "left" if is_right_node else "right"
                sibling_value = self._to_hex(self.levels[x][sibling_index])
                proof.append({sibling_pos: sibling_value})
                index = int(index / 2.)
            return proof

    def validate_proof(self, proof, target_hash, merkle_root):
        merkle_root = bytearray.fromhex(merkle_root)
        target_hash = bytearray.fromhex(target_hash)
        if len(proof) == 0:
            return target_hash == merkle_root
        else:
            proof_hash = target_hash
            for p in proof:
                try:
                    # the sibling is a left node
                    sibling = bytearray.fromhex(p['left'])
                    proof_hash = self.hash_function(sibling + proof_hash).digest()
                except:
                    # the sibling is a right node
                    sibling = bytearray.fromhex(p['right'])
                    proof_hash = self.hash_function(proof_hash + sibling).digest()
            return proof_hash == merkle_root

class Block:
    """A Single Block"""
    def __init__(self):
        self.PrevHash = '0'
        self.RootHash = '0'
        self.BlockHash = '0'
        self.BlockHeight = 0
        self.TXs = []
    def caculateHash(self):
        mt = MerkleTools(hash_type="sha256")
        for tx in self.TXs:
            mt.add_leaf(tx.Hash)
        mt.make_tree()
        self.RootHash = mt.get_merkle_root()
        sha_gen = hashlib.sha256()
        if self.RootHash != None:
            sha_gen.update(str.encode(self.PrevHash + self.RootHash))
        else:
            sha_gen.update(str.encode(self.PrevHash))
        self.BlockHash = sha_gen.hexdigest()

class Tx:
    """A Transaction Record"""
    def __init__(self):
        self.From = ''
        self.To = ''
        self.Value = 0
        self.Hash = ''
    def caculateHash(self):
        sha_gen = hashlib.sha256()
        sha_gen.update(str.encode(self.From+self.To+str(self.Value)))
        self.Hash = sha_gen.hexdigest()

app = Flask(__name__)
blockchain = []
currentBlock = Block()
balance_table = dict()
# Erase old log data
open('log.txt', 'w').close()


@app.route('/')
def mainPage():
    return render_template('index.html', blockchain = blockchain)


@app.route('/addtx', methods=['POST'])
def addTX():
    # TODO:check parameter exist
    global currentBlock
    try:
        sender = request.form['from_addr']
        receiver = request.form['to_addr']
        amount = int(request.form['value'])
        tx = Tx()
        if sender not in balance_table:
            balance_table[sender] = 100
        if receiver not in balance_table:
            balance_table[receiver] = 100
        if balance_table[sender] >= amount:
            balance_table[sender] -= amount;
            balance_table[receiver] += amount;
            tx.From = sender
            tx.To = receiver
            tx.Value = amount
            tx.caculateHash()
            currentBlock.TXs.append(tx)
            writeLog('TX : ${0} {1} -> {2}\n'.format(str(amount),sender,receiver))
            return redirect('/')
        else:
            return render_template('error.html',
                                msg = 'Sender\'s balance is not enough.')
    except KeyError:
        return render_template('error.html',
                            msg = 'Parameter is not valid.')


@app.route('/log')
def dumpLog():
    logfile = open('log.txt', 'r')
    log = logfile.read()
    logfile.close()
    return Response(log, mimetype='text/plain')


def newBlock():
    global currentBlock
    chain_length = len(blockchain)
    currentBlock.PrevHash = blockchain[chain_length-1].BlockHash
    currentBlock.BlockHeight = chain_length+1
    currentBlock.caculateHash()
    blockchain.append(currentBlock)
    writeLog('[Block #{0}] Prev={1} Hash={2}\n'.format(
                    currentBlock.BlockHeight,
                    currentBlock.PrevHash,
                    currentBlock.BlockHash))
    currentBlock = Block()
    threading.Timer(10, newBlock).start()
    return


def writeLog(logStr):
    logfile = open('log.txt', 'a')
    logfile.write(logStr)
    logfile.close()


if __name__ == '__main__':
    genesisBlock = Block()
    genesisBlock.PrevHash = '0'
    genesisBlock.BlockHeight = 1
    genesisBlock.caculateHash()
    blockchain.append(genesisBlock)
    writeLog('[Block #{0}] Prev={1} Hash={2}\n'.format(
                    genesisBlock.BlockHeight,
                    genesisBlock.PrevHash,
                    genesisBlock.BlockHash))
    threading.Timer(10, newBlock).start()
    #app.debug = True
    app.run(host='0.0.0.0', port=8000)
