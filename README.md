# Boolean Network Builder

## What this is
A Python tool to **build Boolean gene regulatory networks**: define components (genes), add definite/optional interactions, specify named conditions, and assemble time-bounded experiments. It also integrates **regulation rules** per node

---

## Features
- Add components with allowed **regulation rule IDs** (e.g., `1-3` or `1,2,4`)
- Add **definite** and **optional** interactions (positive/negative)
- Define reusable **named conditions** (e.g., `start`, `target`)
- Build **experiments** as sequences of (time → assignments)
- Generate per-node **regulation condition dictionaries** (`R1`, `R2`, …) you can inspect or export

---

## Example

```python
from BoolNetwork import BoolNetwork

bn = BoolNetwork()

# 1) Components (allowed regulation IDs)
bn.add_component("A", "1-2")
bn.add_component("B", "1,2,3")

# 2) Interactions: (src, dst, sign, optionalFlag)
bn.add_interaction(("A", "B", "positive", "True"))    # optional
bn.add_interaction(("B", "A", "negative", "False"))   # definite

# 3) Named conditions (reusable assignments)
bn.add_condition(["A=1", "B=0"], "start")
bn.add_condition(["A=0", "B=1"], "target")

# 4) Experiments: ["t0", "condName", "t1", "condName", ...]
bn.add_experiment(["0", "start", "5", "target"])

# 5) Build regulation dictionaries (no model checking)
bn.eval_regulation_conditions()

# Inspect results
print("Components:", list(bn.components.keys()))
print("Experiments:", bn.experiments)
print("Regulation dict keys:", list(bn.regConds.keys())[:5])
print("Example rules for A at exp 0:", bn.regConds.get("A0", {}))
