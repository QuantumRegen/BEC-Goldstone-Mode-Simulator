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

Requirements
```bash
pip install numpy scipy matplotlib pandas plotly
