# Dr. Kaznachey
# Ryan Brooks
# G00957159
# CS 580
#
# This program...
# (1) Implements the AC-3 algorithm to enforce arc-consistency for the CSP
# (2) Implements my Bayesian Network
# (3) Computes the joint probability Pr[WA=red, NT=blue, SA=green, Q=yellow, NSW=red, V=blue, T=yellow]

from collections import deque
from fractions import Fraction

# ------------------------------------------------------------
# 1) CSP and AC-3
# ------------------------------------------------------------

# Variables (regions)
VARS = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]

# Domains (4 colors for each variable)
COLORS = ["r", "g", "b", "y"]
DOMAINS = {v: set(COLORS) for v in VARS}

# Constraints (adjacencies) as "not-equal" binary constraints
ADJ = {
    ("WA", "NT"), ("WA", "SA"),
    ("NT", "Q"), ("NT", "SA"),
    ("Q", "SA"), ("Q", "NSW"),
    ("NSW", "SA"), ("NSW", "V"),
    ("V", "SA"),
}
# Make the graph undirected (add both directions)
ARC_SET = set()
for (a, b) in ADJ:
    ARC_SET.add((a, b))
    ARC_SET.add((b, a))

def revise(xi, xj, domains):
    # Revise domain of xi wrt xj for the constraint xi != xj.
    removed = False
    to_remove = set()
    for x in domains[xi]:
        # keep x if there exists some y in Dj with y != x
        if not any((y != x) for y in domains[xj]):
            to_remove.add(x)
    if to_remove:
        domains[xi] -= to_remove
        removed = True
    return removed

def ac3(domains):
    # AC-3 enforcing arc consistency for not-equal constraints.
    queue = deque(ARC_SET)
    domains = {v: set(vals) for v, vals in domains.items()}  # copy
    while queue:
        (xi, xj) = queue.popleft()
        if revise(xi, xj, domains):
            if not domains[xi]:
                return False, domains  # inconsistency
            # Add neighbors (except xj) back on the queue
            for (xk, xl) in ARC_SET:
                if xl == xi and xk != xj:
                    queue.append((xk, xi))
    return True, domains

# ------------------------------------------------------------
# 2) Bayesian Network
# ------------------------------------------------------------
# Structure (parents for each node):
PARENTS = {
    "SA": [],
    "WA": ["SA"],
    "NT": ["SA", "WA"],
    "Q":  ["SA", "NT"],
    "NSW":["SA", "Q"],
    "V":  ["SA", "NSW"],
    "T":  [],
}

def pr_SA(color):
    # Uniform prior
    return Fraction(1, 4)

def pr_T(color):
    # Uniform prior
    return Fraction(1, 4)

def pr_child_given_parents(child_color, parent_colors):
    # Rule CPT:
    #   - Exclude any parent colors.
    #   - If both parents same -> uniform over remaining 3 colors (1/3).
    #   - If parents differ -> uniform over remaining 2 colors (1/2).
    #   - If one parent -> uniform over remaining 3 colors (1/3).
    if len(parent_colors) == 0:
        raise ValueError("Use pr_SA/pr_T for root nodes.")
    disallowed = set(parent_colors)
    if child_color in disallowed:
        return Fraction(0, 1)
    remaining = set(COLORS) - disallowed
    return Fraction(1, len(remaining))

def pr_node(node, value, assignment):
    # Return Pr[node=value | parents].
    ps = PARENTS[node]
    if not ps:
        if node == "SA":
            return pr_SA(value)
        elif node == "T":
            return pr_T(value)
        else:
            raise ValueError("Unknown root node")
    parent_colors = [assignment[p] for p in ps]
    return pr_child_given_parents(value, parent_colors)

def joint_probability(assignment):
    # Multiply local probabilities in topological order.
    order = ["SA", "WA", "NT", "Q", "NSW", "V", "T"]
    p = Fraction(1, 1)
    for n in order:
        p *= pr_node(n, assignment[n], assignment)
    return p

# ------------------------------------------------------------
# 3) Run everything
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=== AC-3 on the Australia CSP (4 colors) ===")
    ok, reduced = ac3(DOMAINS)
    print("Arc-consistent:", ok)
    for v in sorted(reduced):
        print(f"  {v}: {sorted(reduced[v])}")
    print()

    # Joint probability
    query = {
        "WA": "r",
        "NT": "b",
        "SA": "g",
        "Q":  "y",
        "NSW":"r",
        "V":  "b",
        "T":  "y",
    }
    jp = joint_probability(query)

    print("=== Bayesian Network Joint Probability ===")
    print("Assignment:", query)
    print("Exact (fraction):", jp)
    print("Decimal:", float(jp))
