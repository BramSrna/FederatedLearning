# Proof Of Simulation
Proof of simulation is similar to a proof of work system (https://en.wikipedia.org/wiki/Proof_of_work) where the work performed is executing a simulator. The main use case is in federated learning. A sample scenario is as follows:
- There are several nodes working on optimizing a task. The nodes all have copies of the task being optimized as well as a simulator that they can use for evaluation.
- The nodes all locally apply some sort of machine learning, such as reinforcement learning, to optimize the task using the simulator. When a node find a better version of the task (runs faster, covers more corner cases, etc), it creates a block containing the improved task alongside proof of executing against the simulator.
- The block is pushed to all of the nodes and the process repeats. This continues until a predetermined stopping point.

This project contains an implementation of the core proof of simulation framework.

# Sample Use Case Pseudocode
```
simulator = Simulator()
start_task = Task()
end_node_length = 5

pos_blockchain = PosBlockchain(simulator, start_task, end_node_length)

num_nodes = 3
nodes = []
threads = []

while len(nodes) < num_nodes:
    new_node = Node(pos_blockchain)
    new_thread = Thread(target=new_node.execute)

    nodes.append(new_node)
    threads.append(new_thread)
    
for thread in threads:
    thread.join()

final_task = nodes[0].get_task()
```

# Simulator
Simulators are similar to state machines. When in state X, action Y will lead to state Z. In the context of over the air simulator changes in a proof of simulation framework, simulators are a tool used for verifying new functions using the saved test cases.

# Block Types
- Simulator config updates
- - Need to ensure that new simulator performs at least as well as the current one
- - Use the current function to validate the simulator
- Test Cases Updates
- - These shall be additive only
- - Tests can be functionality, performance based, etc
- - Validate new test cases against current function
- Function Updates
- - Validate using the simulator and test cases