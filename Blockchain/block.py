from datetime import datetime
from hashlib import sha256


class Block:
    def __init__(self, index: int, data: str, previous_hash: str):
        self.index = index
        self.timestamp = int(datetime.timestamp(datetime.utcnow()))
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.hash_block()

    def hash_block(self) -> str:
        block_as_list = self.to_list()
        hash_sha256 = sha256(str(block_as_list).encode("utf-8"))
        return hash_sha256.hexdigest()

    def mine_block(self, difficulty: int):
        print("Mining...")
        while self.hash[:difficulty] != "0" * difficulty:
            current_timestamp = int(datetime.timestamp(datetime.utcnow()))
            if self.timestamp != current_timestamp:
                self.timestamp = current_timestamp
                self.nonce = 0
            self.nonce += 1
            self.hash = self.hash_block()
        return self

    def is_valid(self, difficulty: int) -> bool:
        if self.hash[:difficulty] != "0" * difficulty:
            return False
        elif self.hash != self.hash_block():
            return False
        return True

    def to_list(self, include_hash: bool = False) -> list:
        block_as_list = [
            str(self.index),
            str(self.timestamp),
            str(self.data),
            str(self.previous_hash),
            str(self.nonce),
        ]
        if include_hash:
            block_as_list.append(self.hash)
        return block_as_list

    def populate_from_list(self, block_as_list: list):
        self.index = int(block_as_list[0])
        self.timestamp = int(block_as_list[1])
        self.data = block_as_list[2]
        self.previous_hash = block_as_list[3]
        self.nonce = int(block_as_list[4])
        self.hash = self.hash_block()
        return self

    def __repr__(self):
        return "Block<Hash: {}, Nonce: {}>".format(self.hash, self.nonce)

    def __str__(self):
        str_block = ""
        str_block += str(self.index) + "\t"
        str_block += str(datetime.utcfromtimestamp(self.timestamp)) + "\t"
        if len(self.data) > 16:
            str_block += str(self.data[:16]) + "..."
        else:
            str_block += str(self.data).ljust(16)
        str_block += "\t"
        str_block += str(self.previous_hash)[:16] + "...\t"
        str_block += str(self.nonce).ljust(16) + "\t"
        str_block += str(self.hash)[:16] + "..."
        return str_block
