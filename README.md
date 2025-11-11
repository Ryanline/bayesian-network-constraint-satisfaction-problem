# Description
Implements Constraint Satisfaction Problem (CSP) logic and a Bayesian Network to solve a map-coloring dilemma. Implements the AC-3 algorithm to guarantee arc-consistency, constructs conditional probability tables, and computes joint probabilities for given color assignments.

# Implements
- **CSP** Algorithmic logic
- **AC-3** for arc consistency
- **Bayesian Network** with a compact structure and custom Conditional Probability Tables

## Highlights
- AC‑3 implementation for enforcing arc consistency on the map-coloring CSP.
- Bayesian Network with nodes `{SA, WA, NT, Q, NSW, V, T}` and local conditional tables.
- Computes the joint probability  
  `Pr[WA=r, NT=b, SA=g, Q=y, NSW=r, V=b, T=y] = 1/768`.

## Repo Layout
```
.
├── docs/
│   ├── Bayesian-Network.pdf
│   ├── Conditional-Probability-Table.pdf
│   └── HW3-writeup.pdf
├── src/
│   └── australia_csp_bn.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

- **docs/** contains the original PDFs for the Bayesian network diagram, CPTs, and the write‑up.
- **src/** has the runnable Python implementation (AC‑3 + BN + joint probability).

# Expected output:
- AC‑3 arc‑consistency result with reduced domains.
- Exact fraction and decimal for the joint probability query.

## License
MIT — see [LICENSE](./LICENSE).