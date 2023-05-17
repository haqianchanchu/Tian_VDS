
import parameters
import structure
import json
import analyzer
import Beacon

CENTER = 100
NODESIZE = 100
# import numpy as np
USER_NUMBER = parameters.USER_NUMBER
MAX_OUTPUTIP = parameters.MAX_OUTPUTIP
MAX_INPUTIP = parameters.MAX_INPUTIP
R = parameters.EPOCH
CP_K = parameters.CP_K
MAX_SLOT = parameters.MAX_SLOT
EP = parameters.EPISLON
VOTELEN = 10
VOTESPACE = 10
class Tree(analyzer.Tree):
    """docstring for tree"""
    def __init__(self, block:str):
        super(Tree, self).__init__(block)
    def vote_judge(self):
        Beacon.init_U(EP)
        while len(Beacon.rand_list)<MAX_SLOT:
            Beacon.select(len(Beacon.rand_list)+1)
        i = 0
        while i<MAX_SLOT:
            value = 0
            j = 0
            while j<VOTELEN:
                sl = i+j
                if Beacon.select(sl) == Beacon.corrupt and Beacon.select(sl+1) == Beacon.corrupt:
                    value -= 2
                elif Beacon.select(sl) == Beacon.corrupt:
                    value -= 1
                else:
                    value += 1
                j+= 1
            print("value"+str(value))
            if value <= 0:
                return "error"
            i += VOTESPACE
        return "right"

    def child_append(self, child):
        real_child = []
        used_block = []
        pre_block = structure.Block.get(self.block)
        pre_head = structure.Block_head.get(pre_block.head)
        old_list = [pre_head.old_state, pre_head.new_state, pre_head.d,pre_head.sigma_d, 
            pre_head.t, pre_head.sigma_t, pre_block.body]
        st = self.old_state = structure.get_hash256(old_list)
        for block in child:
            block = structure.Block.get(block)
            head = structure.Block_head.get(block.head)
            if head.old_state == st:
                # print("sl:"+str(self.sl)+str(block.sl))
                real_child.append(Tree(block.put()))
                used_block.append(block.put())
        self.child = real_child
        # print(len(real_child))
        return used_block
    def chain_judge(self):
        center = 0
        if len(self.child) > 1:
            print(self.sl)
            sum = 0
            for node in self.child:
                if node.length()> 2*CP_K:
                    sum += 1
            if sum > 1:
                return 0
            judge_ans = 1
            for node in self.child:
                ans_list *= node.chain_judge()
            return ans_list
        elif len(self.child)==1:
            return self.child[0].chain_judge()
        else :
            return 1
    def length(self, mylength = 0):
        if len(self.child) == 0:
            return 0
        length_list = []
        for node in self.child:
            length_tem = node.length() 
            length_list.append(length_tem)
        mylength += max(length_list)+1
        return mylength

def main():
    with open("block_chain_table", "r") as f:
        chain_table = f.read()
    chain_table = json.loads(chain_table)
    for chain in chain_table:
        for block in chain:
            block  = structure.Block.get(block)
            print("sl:"+str(block.sl))
    tree = Tree(chain_table[0][0])
    for chain in chain_table:
        del chain[0]
    analyzer.create_tree(chain_table, tree)
    # print(chain_table)
    ans1 = tree.chain_judge()
    ans2 = tree.vote_judge()
    print(ans1)
    print(ans2)


if __name__ == '__main__':
    main()