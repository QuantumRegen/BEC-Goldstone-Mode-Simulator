## Theoretical Backbone

This toy is a minimal playground for spontaneous symmetry breaking + Goldstone emergence.

### Core Equation (2D GPE)

i ℏ ∂_t ψ = [- (ℏ²/2m) ∇² + V_trap(x,y) + g |ψ|² ] ψ

Imaginary-time version (for ground state):

∂_τ ψ = [-∇²/2 + V_trap + g |ψ|² - μ] ψ    (with norm preserved)

### Added μ_I drive (pion-like condensation proxy)

V → V_eff = V_trap - λ μ_I² |ψ|²

→ effective potential for n = |ψ|² becomes concave when μ_I large → density instability → condensation

### Symmetry & Order Parameter

ψ = √n e^{iθ}

Global U(1): ψ → e^{iα} ψ

In double-well:
- Low μ_I: two local condensates → two independent phases θ_L, θ_R
- High μ_I: single coherent condensate → one global θ → U(1) broken spontaneously

Goldstone mode: long-wavelength θ fluctuations → ω(k) ≈ c |k| (c = √(g n) sound speed)

### Phase Slip / Rigidity

When lobes merge, central phase flattens (low energy cost to twist θ) → "slip" = soft relative phase mode  
→ precursor to full Goldstone boson (phonon in BEC, pion in QCD analog)

Tiny asymmetry (well depths -5.0 vs -4.8) seeds direction → amplified above critical μ_I → runaway dominance of one side (spontaneous choice)

This echoes chiral rotation + pion BEC at finite isospin density in QCD effective theories.
