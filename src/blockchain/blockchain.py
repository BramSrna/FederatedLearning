class Blockchain(object):
    def __init__(self):
        self.blocks = []

    def get_blocks(self):
        return self.blocks
    
    def is_empty(self):
        return len(self.blocks) == 0
    
    def get_length(self):
        return len(self.blocks)
    
    def add_block(self, new_block):
        print("HERE_3")
        if new_block not in self.blocks:
            print("HERE_4")
            self.blocks.append(new_block)

    def get_newest_block(self):
        return self.blocks[-1]