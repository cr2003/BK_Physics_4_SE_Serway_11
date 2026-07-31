# Helper functions

import matplotlib.pyplot as plt
import numpy as np


def fmt_vec(v, precision=2, type="f"):
    """Format the output of a vector with the specified precision"""
    return f"<{v.x:.{precision}{type}}, {v.y:.{precision}{type}}, {v.z:.{precision}{type}}>"


def math_to_bearing(theta):
    """Converts mathematical angle (degrees) to navigation bearing (degrees)."""
    return (90 - theta) % 360


def plot_vector(magnitude, theta_deg, origin=(0, 0), ax=None, color="b", label=None):
    """
    Dibuja un vector 2D a partir de su magnitud y ángulo.

    Parámetros:
        magnitude : float - módulo del vector
        theta_deg : float - ángulo en grados (medido desde el eje X positivo)
        origin    : tuple - punto de origen del vector (x0, y0)
        ax        : matplotlib Axes - si es None, crea una figura nueva
        color     : str - color del vector
        label     : str - etiqueta para la leyenda

    Retorna:
        ax, (vx, vy) - los ejes usados y las componentes del vector
    """
    theta_rad = np.radians(theta_deg)
    vx = magnitude * np.cos(theta_rad)
    vy = magnitude * np.sin(theta_rad)
    x0, y0 = origin

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_aspect("equal")
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.axvline(0, color="gray", linewidth=0.5)
        ax.grid(True, linestyle="--", alpha=0.5)

    ax.quiver(
        x0,
        y0,
        vx,
        vy,
        angles="xy",
        scale_units="xy",
        scale=1,
        color=color,
        label=label,
        width=0.007,
    )

    # Ajustar límites automáticamente
    margin = magnitude * 1.3
    ax.set_xlim(
        min(ax.get_xlim()[0], x0 - margin), max(ax.get_xlim()[1], x0 + vx + margin)
    )
    ax.set_ylim(
        min(ax.get_ylim()[0], y0 - margin), max(ax.get_ylim()[1], y0 + vy + margin)
    )

    if label:
        ax.legend()

    return ax, (vx, vy)


def plot_vector_xy(vx, vy, origin=(0, 0), ax=None, color="g", label=None):
    """
    Dibuja un vector 2D a partir de sus componentes cartesianas.

    Parámetros:
        vx, vy    : float - componentes x e y del vector
        origin    : tuple - punto de origen del vector (x0, y0)
        ax        : matplotlib Axes - si es None, crea una figura nueva
        color     : str - color del vector
        label     : str - etiqueta para la leyenda

    Retorna:
        ax, (magnitude, theta_deg) - los ejes usados y la magnitud/ángulo equivalentes
    """
    x0, y0 = origin
    magnitude = np.hypot(vx, vy)
    theta_deg = np.degrees(np.arctan2(vy, vx))

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_aspect("equal")
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.axvline(0, color="gray", linewidth=0.5)
        ax.grid(True, linestyle="--", alpha=0.5)

    ax.quiver(
        x0,
        y0,
        vx,
        vy,
        angles="xy",
        scale_units="xy",
        scale=1,
        color=color,
        label=label,
        width=0.007,
    )

    margin = magnitude * 1.3
    ax.set_xlim(
        min(ax.get_xlim()[0], x0 - margin), max(ax.get_xlim()[1], x0 + vx + margin)
    )
    ax.set_ylim(
        min(ax.get_ylim()[0], y0 - margin), max(ax.get_ylim()[1], y0 + vy + margin)
    )

    if label:
        ax.legend()

    return ax, (magnitude, theta_deg)


import math


def oom(x):
    """
    Returns the numerical value (10^n) of the nearest order of magnitude
    using the sqrt(10) ~ 3.162 rounding rule.

    Preserves AstroPy Quantity types and their associated units.
    """
    has_unit = hasattr(x, "unit") and hasattr(x, "value")

    # Extract raw numeric value
    x_val = x.value if has_unit else x
    x_abs = abs(float(x_val))

    if x_abs == 0:
        oom_numeric = 0.0
    else:
        # Calculate 10^exponent using the rounding rule
        exponent = round(math.log10(x_abs))
        oom_numeric = 10.0**exponent

    # Return as AstroPy Quantity if input was one, else plain float
    return oom_numeric * x.unit if has_unit else oom_numeric
