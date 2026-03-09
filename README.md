Requires:

numpy
scipy
matplotlib
json
pandas
plotly

This is a sandbox BEC dynamics simulator. It was iterated from my original script with Grok! and my BEC focused studies.
Go dynamic- :) 

BEC Goldstone Mode Simulator

2D Gross-Pitaevskii equation solver for a trapped double-well Bose-Einstein Condensate (BEC).  
Focus: excite and visualize **Josephson plasma oscillations** (macroscopic manifestation of the U(1) **Goldstone mode**).

Features
- Imaginary-time relaxation to ground state
- Configurable excitations: phase kick, density dip, linear tilt, vortex imprint
- Real-time propagation with data collection (lobe populations, COM x, relative phase)
- JSON export for post-processing
- Animation (GIF/MP4) + interactive Plotly dashboard

UPDATED::

Goldstone Modes Toy Models

Exploring spontaneous symmetry breaking, Goldstone mode emergence, phase slips, and condensation transitions in minimal toy systems (inspired by BEC and finite-isospin QCD).

Current Focus
- 1D Gross-Pitaevskii equation (imaginary-time evolution) with double-well potential
- μ_I (isospin chemical potential) drive for pion-like condensation
- Tiny explicit asymmetry to seed spontaneous symmetry breaking
- Phase slip / rigidity visualization during merging transition

Key Phenomena Observed
- Density-driven lobe merging and central condensate formation
- Amplification of tiny bias → runaway dominance of one side
- Central phase flattening → Goldstone mode softening / slip
- High phase rigidity in condensed phase (variance ~0 in dense core)
- Noise resilience test → quick relaxation back to ground state

This mirror is actually real... ?
