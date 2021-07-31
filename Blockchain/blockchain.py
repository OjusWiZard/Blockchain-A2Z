from csv import reader, writer

from block import Block


class Blockchain:
    def __init__(self, blocks_filename:str, difficulty=4):
        self.blocks_filename = blocks_filename
        self.difficulty = difficulty
        self.blocks_file_append = open(self.blocks_filename, "a")
        self.blocks_file_read = open(self.blocks_filename, "r")
        self.blocks_writer = writer(self.blocks_file_append, delimiter="|")
        self.blocks_reader = reader(self.blocks_file_read, delimiter="|")

        if self.get_last_block() is None:
            self.add_block(self.genesis_block())

    def genesis_block(self) -> Block:
        genesis_block = Block(0, "This is just the Beginning", "0" * 64)
        genesis_block.mine_block(self.difficulty)
        return genesis_block

    def add_block(self, data) -> Block:
        last_block = self.get_last_block()
        if not last_block:
            last_block = self.genesis_block()
        block = Block(last_block.index + 1, data, last_block.hash)
        if not block.mine_block(self.difficulty):
            return None
        self.blocks_writer.writerow(block.to_list(include_hash=True))
        self.blocks_file_append.flush()
        return block

    def is_valid(self) -> bool:
        self.blocks_reader = reader(open(self.blocks_filename, "r"), delimiter="|")
        previous_block_as_list = next(self.blocks_reader, None)
        if previous_block_as_list is None:
            return True
        else:
            previous_block = Block(0, "temp", "0").populate_from_list(
                previous_block_as_list
            )
            if not previous_block.is_valid(self.difficulty):
                return False

        while True:
            current_block_as_list = next(self.blocks_reader, None)
            if current_block_as_list is None:
                return True
            else:
                current_block = Block(0, "temp", "0").populate_from_list(
                    current_block_as_list
                )
                if not current_block.is_valid(self.difficulty):
                    return False

            if previous_block.hash != current_block.previous_hash:
                return False
            previous_block = current_block

    def get_last_block(self) -> Block:
        with open(self.blocks_filename, "r") as blocks_file:
            lines = [line for line in blocks_file]
            if not lines:
                return None
            else:
                block_as_list = lines[-1].split("|")
                return Block(0, "temp", "0").populate_from_list(block_as_list)

    def get_chain(self) -> list:
        self.blocks_reader = reader(open(self.blocks_filename, "r"), delimiter="|")
        return [block for block in self.blocks_reader]

    def __str__(self):
        str_blockchain = ""
        for block in self.get_chain():
            str_blockchain += (
                str(Block(0, "temp", "0").populate_from_list(block)) + "\n"
            )
        return str_blockchain

    def __del__(self):
        self.blocks_file_append.close()
        self.blocks_file_read.close()
