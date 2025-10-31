# Boolean Network Model Generator

## Overview
This project is a Python-based tool that builds, explores, and verifies **Boolean gene regulatory networks** using the **nuXmv model checker**.  
It automatically generates SMV (Symbolic Model Verification) files from network definitions and systematically tests which configurations of optional gene interactions produce experimentally valid outcomes.

The goal is to help researchers and students analyze **how different regulatory edges affect network behavior** — and to automatically discover which combinations are logically consistent with observed experimental data.

---

## How It Works
The tool runs in two main stages:

1. **Network Construction (`BoolNetwork`)**
   - Builds a Boolean network of genes and interactions.
   - Supports *definite* (always present) and *optional* (uncertain) regulatory edges.
   - Defines experiments that represent target states the network should achieve.
   - Generates all possible interaction permutations and logical update conditions for each component.

2. **Model Generation and Verification (`ToSmv`)**
   - For each possible network configuration, converts the Boolean logic into an `.smv` model file.
   - Uses `nuXmv` to check if all experiments can be satisfied under that configuration.
   - Records which configurations successfully reproduce the experimental outcomes.
   - Displays results and saves logs for further analysis.

---

## Main Component

| File | Description |
|------|--------------|
| **BoolNetwork.py** | Builds and manages the Boolean network structure, experiments, and all permutations of optional interactions. |

---

## Key Concepts

- **Definite vs. Optional Interactions**  
  Definite interactions always exist in the network, while optional ones are toggled on/off to explore different possible structures.

- **Experiments**  
  Each experiment defines:
  - Initial values for each component (0/1).
  - A target state to reach within a given number of time steps.

- **Regulation Conditions**  
  Each component has a set of possible Boolean rules (`R1`, `R2`, `R3`, …) that define how its next state depends on other nodes.

---

## Example Workflow

```python
from BoolNetwork import BoolNetwork
from ToSmv import ToSmv

# Step 1: Build the network
bn = BoolNetwork()
bn.add_component("A", "1-2")
bn.add_component("B", "1,2,3")
bn.add_interaction(("A", "B", "positive", "True"))  # optional edge
bn.add_interaction(("B", "A", "negative", "False")) # definite edge
bn.add_condition(["A=1", "B=0"], "start")
bn.add_condition(["A=0", "B=1"], "target")
bn.add_experiment(["0", "start", "5", "target"])
bn.eval_regulation_conditions()
