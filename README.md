# Ontological Impoverishment: Reachable Bodies and the Freedom to Take Form

The paper defines ontological impoverishment as the institutionally avoidable foreclosure of reachable ways of being embodied, keeps it distinct from material poverty, and formalises it as a reachable set under four constraints: physical possibility, developmental reachability, lived integration and political accessibility. It reads Heidegger, the experiments of Michael Levin and colleagues, morphological-freedom theory and xenofeminism against that structure, and tests the claim that resistance to bodily enhancement belongs to the political left with published Pew Research Center aggregates.

[Read the paper](https://piatra.institute/papers/ontological-impoverishment.pdf)

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build ontological-impoverishment`.

## Analysis

`simulation/` re-analyses aggregate tables transcribed from two Pew Research Center reports. See `simulation/README.md`. `check_numerals.py` lists every numeral in the manuscript and checks that it is bound in `claims.yaml`.
