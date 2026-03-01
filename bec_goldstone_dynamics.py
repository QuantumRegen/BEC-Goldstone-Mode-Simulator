"""
BEC Goldstone Mode Simulator - Double-Well Josephson Dynamics
============================================================

Solves 2D time-dependent Gross-Pitaevskii equation (GPE) using split-step Fourier method.
Focus: excite and observe U(1) Goldstone modes (Josephson plasma oscillations / phonons)
in a trapped double-well BEC.

Features:
- Imaginary-time relaxation to ground state
- Configurable excitations (phase kick, density dip, linear tilt, vortex imprint)
- Long real-time propagation
- Collects: lobe populations, center-of-mass, relative phase
- Exports structured JSON for analysis/visualization
- Saves animation (GIF/MP4) and/or PNG sequence

Author: Inspired by user @QuantumRegen / AiCE/Hi
Date: March 2026
"""

import numpy as np
from scipy.fft import fft2, ifft2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import json
import os
from datetime import datetime

# ==================== CONFIGURATION ====================

# Grid & physical parameters (pm units, ħ = m = 1)
Nx = Ny = 256
dx = dy = 0.2
x = dx * (np.arange(Nx) - Nx//2)
y = dy * (np.arange(Ny) - Ny//2)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)

dt = 0.001                  # Time step (keep small for stability)
g = 5000.0                  # Interaction strength (tight healing length)
omega = 10.0                # Trap frequency
barrier_height = 100.0      # Central barrier (controls tunneling)
barrier_width = 0.5         # Barrier Gaussian width

# Evolution settings
imag_steps = 600            # More steps for strong g/barrier convergence
real_steps = 15000          # Long run (~15 time units)
save_every = 50             # ~300 frames

# Excitation choices (set to True/False or adjust values)
EXCITE_PHASE_KICK = True
phase_kick_magnitude = 0.4 * np.pi     # rad, applied to right lobe
phase_kick_x_threshold = 0.5           # x > this gets kick

EXCITE_DENSITY_DIP = False
dip_magnitude = 0.92                   # multiply density by this in right lobe
dip_radius = 2.0                       # pm

EXCITE_TILT = False
tilt_strength = 0.5                    # linear potential gradient (delta * x)

EXCITE_VORTEX = False                  # Phase imprint (winding number 1)

# Output
output_dir = "bec_goldstone_results"
os.makedirs(output_dir, exist_ok=True)
json_filename = "bec_dynamics.json"
gif_filename = "bec_evolution.gif"
mp4_filename = "bec_evolution.mp4"     # Preferred if ffmpeg available

# ==================== POTENTIAL ====================

V = 0.5 * omega**2 * r**2
V += barrier_height * np.exp(-r**2 / (2 * barrier_width**2))

# Optional tilt
if EXCITE_TILT:
    V += tilt_strength * X

# ==================== GPE PROPAGATOR ====================

kx = 2 * np.pi * np.fft.fftfreq(Nx, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(Ny, d=dy)
KX, KY = np.meshgrid(kx, ky)
k2 = (KX**2 + KY**2) / 2

def gpe_step(psi, V, g, dt, k2, imag_time=False):
    """Split-step Fourier propagation (Strang splitting)"""
    # Half nonlinear + potential step
    exp_v = -dt / 2 * (V + g * np.abs(psi)**2)
    if imag_time:
        exp_v = np.real(exp_v)
    else:
        exp_v = 1j * exp_v
    psi = np.exp(exp_v) * psi

    # Full kinetic step
    psi_k = fft2(psi)
    exp_k = np.exp(-dt * k2) if imag_time else np.exp(-1j * dt * k2)
    psi_k *= exp_k
    psi = ifft2(psi_k)

    # Second half nonlinear + potential step
    psi = np.exp(exp_v) * psi

    # Normalize
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx * dy)
    psi /= norm
    return psi

# ==================== INITIAL CONDITION ====================

psi = np.exp(-r**2 / 10) / np.sqrt(np.pi)
psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx * dy)

# ==================== GROUND STATE (IMAGINARY TIME) ====================

print("Relaxing to ground state...")
for i in range(imag_steps):
    psi = gpe_step(psi, V, g, dt, k2, imag_time=True)
    if (i + 1) % 100 == 0:
        print(f"  Imag step {i+1}/{imag_steps}")

print("Ground state ready.")

# ==================== APPLY EXCITATION ====================

if EXCITE_PHASE_KICK:
    phase_mask = (X > phase_kick_x_threshold)
    psi *= np.exp(1j * phase_kick_magnitude * phase_mask)
    print(f"Applied phase kick of {phase_kick_magnitude/np.pi:.2f}π to right lobe")

if EXCITE_DENSITY_DIP:
    dip_mask = (X > phase_kick_x_threshold) & (r < dip_radius)
    psi[dip_mask] *= dip_magnitude
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx * dy)
    print(f"Applied density dip of {dip_magnitude:.2f} to right lobe")

if EXCITE_VORTEX:
    theta = np.arctan2(Y, X)
    psi *= np.exp(1j * theta)  # winding number 1
    print("Applied phase vortex imprint (winding 1)")

# ==================== REAL-TIME EVOLUTION + DATA COLLECTION ====================

data = {
    "metadata": {
        "run_started": datetime.now().isoformat(),
        "dt": dt,
        "g": g,
        "omega": omega,
        "barrier_height": barrier_height,
        "barrier_width": barrier_width,
        "imag_steps": imag_steps,
        "real_steps": real_steps,
        "save_every": save_every,
        "total_time": real_steps * dt,
        "excitations": {
            "phase_kick": EXCITE_PHASE_KICK,
            "density_dip": EXCITE_DENSITY_DIP,
            "tilt": EXCITE_TILT,
            "vortex": EXCITE_VORTEX
        }
    },
    "times": [],
    "left_density": [],
    "right_density": [],
    "com_x": [],
    "rel_phase": []
    # Add "density_snapshots": [] if you want downsampled 2D arrays
}

density_frames = []  # For animation

print("Starting real-time evolution...")
for step in range(real_steps):
    psi = gpe_step(psi, V, g, dt, k2, imag_time=False)

    if step % save_every == 0:
        t = step * dt
        density = np.abs(psi)**2
        density_frames.append(density.copy())

        # Populations
        left_mask = X < 0
        right_mask = X > 0
        left_int = np.sum(density[left_mask]) * dx * dy
        right_int = np.sum(density[right_mask]) * dx * dy

        # Center of mass x
        total_mass = left_int + right_int
        com_x = np.sum(density * X) * dx * dy / total_mass if total_mass > 0 else 0

        # Relative phase (weighted average)
        phase = np.angle(psi)
        left_phase = np.sum(phase[left_mask] * density[left_mask]) / left_int if left_int > 0 else 0
        right_phase = np.sum(phase[right_mask] * density[right_mask]) / right_int if right_int > 0 else 0
        rel_phase = right_phase - left_phase

        data["times"].append(float(t))
        data["left_density"].append(float(left_int))
        data["right_density"].append(float(right_int))
        data["com_x"].append(float(com_x))
        data["rel_phase"].append(float(rel_phase))

        print(f"t = {t:6.3f} | Left: {left_int:.4f} | Right: {right_int:.4f} | Δphase: {rel_phase:.3f}")

# ==================== SAVE JSON ====================

json_path = os.path.join(output_dir, json_filename)
with open(json_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"JSON saved: {json_path}")

# ==================== ANIMATION ====================

if density_frames:
    fig, ax = plt.subplots(figsize=(9, 9))
    im = ax.imshow(density_frames[0], extent=[x.min(), x.max(), y.min(), y.max()],
                   cmap='viridis', vmin=0, vmax=np.max(density_frames[0])*1.1)
    ax.set_title('BEC Density Evolution')
    ax.set_xlabel('x (pm)')
    ax.set_ylabel('y (pm)')
    plt.colorbar(im, ax=ax, label='Density')

    def update(frame):
        im.set_array(density_frames[frame])
        ax.set_title(f'BEC Density - t = {data["times"][frame]:.3f}')
        return [im]

    ani = FuncAnimation(fig, update, frames=len(density_frames), interval=80, blit=True)

    # Try GIF first
    try:
        ani.save(os.path.join(output_dir, gif_filename), writer=PillowWriter(fps=12), dpi=120)
        print(f"GIF saved: {gif_filename}")
    except Exception as e:
        print(f"GIF save failed: {e}")
        # Fallback to PNG sequence
        frame_dir = os.path.join(output_dir, "frames")
        os.makedirs(frame_dir, exist_ok=True)
        for i, dens in enumerate(density_frames):
            fig_temp = plt.figure(figsize=(6,6))
            plt.imshow(dens, extent=[x.min(), x.max(), y.min(), y.max()], cmap='viridis')
            plt.title(f't = {data["times"][i]:.3f}')
            plt.savefig(os.path.join(frame_dir, f"frame_{i:04d}.png"), dpi=150, bbox_inches='tight')
            plt.close(fig_temp)
        print(f"PNG sequence saved to {frame_dir}/")
        print("To make GIF: ffmpeg -framerate 12 -i frames/frame_%04d.png -vf scale=800:-1 bec_evolution.gif")

    plt.show()

# ==================== QUICK PLOT ====================

plt.figure(figsize=(10,6))
plt.plot(data["times"], data["left_density"], label="Left lobe (x<0)")
plt.plot(data["times"], data["right_density"], label="Right lobe (x>0)")
plt.plot(data["times"], data["com_x"], '--', label="COM x")
plt.xlabel("Time")
plt.ylabel("Integrated density / position")
plt.title("Josephson Oscillation & Dipole Mode")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, "population_com.png"), dpi=150)
plt.show()

print("Run complete. Check output in:", output_dir)