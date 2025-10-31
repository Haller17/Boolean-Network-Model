# Boolean Network Model

## Overview
This project is a Python tool for **building Boolean gene regulatory networks** — systems where components (like genes) have binary states (1/0) and influence one another through positive or negative interactions.  

It lets you define network components, specify definite and optional regulatory edges, set up experimental conditions, and automatically generate regulation logic for each component.  
The focus here is on *constructing* and *exploring* the network structure

---

## Features
- Define Boolean components and their possible regulation rule IDs (e.g., `"1-3"` or `"1,2,4"`).  
- Add **definite** and **optional** regulatory interactions with direction and sign.  
- Create **named conditions** (sets of variable assignments like `"A=1, B=0"`).  
- Combine these into **experiments** — specifying how the system evolves over time.  
- Generate a structured set of **regulation condition dictionaries** for every node.  
---

## Example Usage

```python
from BoolNetwork import BoolNetwork

# Initialize the network
bn = BoolNetwork()

# 1. Define components and their allowed regulation IDs
bn.add_component("A", "1-2")
bn.add_component("B", "1,2,3")

# 2. Add interactions: (source, target, sign, isOptional)
bn.add_interaction(("A", "B", "positive", "True"))    # optional edge
bn.add_interaction(("B", "A", "negative", "False"))   # definite edge

# 3. Add named conditions
bn.add_condition(["A=1", "B=0"], "start")
bn.add_condition(["A=0", "B=1"], "target")

# 4. Define experiments as time-labeled sequences
bn.add_experiment(["0", "start", "5", "target"])

# 5. Generate the regulation logic (no model checking)
bn.eval_regulation_conditions()

# results
print("Components:", list(bn.components.keys()))
print("Experiments:", bn.experiments)
print("Example rules for A0:", bn.regConds.get("A0", {}))
