"""Static PNG figures from real measurements, ready to embed in Markdown."""

import math
from pathlib import Path


def _figure(width: float, height: float):
    # Lazy imports let model/checkpoint utilities work without importing plotting.
    # Direct Agg canvases render without a desktop window or a display server.
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    figure = Figure(figsize=(width, height), facecolor="#faf9f6", layout="constrained")
    FigureCanvasAgg(figure)
    return figure


def _save(figure, path: str | Path) -> Path:
    target = Path(path)
    if target.suffix.lower() not in (".png", ".svg"):
        raise ValueError("Plot output must end in .png or .svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(target, dpi=160, facecolor=figure.get_facecolor())
    return target


def write_loss_plot(metrics: list[dict], path: str | Path) -> Path:
    """Plot recorded fixed-window cross entropy with a zero-based vertical axis."""
    if not metrics:
        raise ValueError("At least one evaluation record is needed for a loss plot")
    values = [float(row[name]) for row in metrics for name in ("train_loss", "val_loss")]
    if not all(math.isfinite(value) and value >= 0 for value in values):
        raise ValueError("Loss values must be nonnegative and finite")
    figure = _figure(8.5, 4.8)
    axis = figure.subplots()
    axis.set_facecolor("#faf9f6")
    steps = [int(row["step"]) for row in metrics]
    for column, color, label in (
        ("train_loss", "#196d72", "Training windows"),
        ("val_loss", "#ac552c", "Validation windows"),
    ):
        axis.plot(steps, [float(row[column]) for row in metrics], color=color, marker="o", markersize=4, linewidth=2, label=label)
    axis.set_title("Next-character prediction loss\nFixed evaluation windows; each dot is a recorded measurement", loc="left", fontsize=13, pad=15)
    axis.set_xlabel("Optimizer steps")
    axis.set_ylabel("Cross entropy (nats) · lower is better")
    axis.set_ylim(0, max(0.1, max(values) * 1.1))
    axis.set_xlim(0, max(1, max(steps)))
    axis.grid(axis="y", color="#dcdedb", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False)
    return _save(figure, path)


def visible_character(character: str) -> str:
    return {" ": "space", "\n": "\\n", "\t": "\\t", "\r": "\\r", "\\": "\\\\"}.get(character, character)


def write_attention_plot(weights: list[list[float]], characters: list[str], path: str | Path, *, head: int = 0) -> Path:
    """True first-block probabilities: rows=query/receiver, columns=key/source."""
    from matplotlib.colors import LinearSegmentedColormap

    length = len(characters)
    if not length or len(weights) != length or any(len(row) != length for row in weights):
        raise ValueError("Attention must be a square matrix matching the text length")
    if any(not math.isfinite(value) or value < -1e-6 or value > 1 + 1e-6 for row in weights for value in row):
        raise ValueError("Attention weights must be finite probabilities")
    side = max(6.4, 3.0 + length * 0.30)
    figure = _figure(side + 1.0, side)
    axis = figure.subplots()
    colors = LinearSegmentedColormap.from_list("attention_probability", ["#f2f5f4", "#1c6070"])
    displayed = axis.imshow(weights, vmin=0, vmax=1, cmap=colors, interpolation="nearest")
    labels = [f"{index}: {visible_character(character)}" for index, character in enumerate(characters)]
    label_size = 10 if length <= 12 else 8
    axis.set_xticks(range(length), labels, fontsize=label_size)
    axis.set_yticks(range(length), labels, fontsize=label_size)
    axis.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False, length=0, pad=6)
    axis.xaxis.set_label_position("top")
    axis.set_xlabel("Key / source position", labelpad=12)
    axis.set_ylabel("Query / receiving position", labelpad=12)
    figure.suptitle(f"Actual first-block attention · head {head}\nRows receive information; columns supply it. Each row sums to one.", fontsize=13)
    if length <= 12:
        for query, row in enumerate(weights):
            for key, weight in enumerate(row):
                axis.text(key, query, f"{weight:.2f}", ha="center", va="center", color="white" if weight > 0.62 else "#24373c", fontsize=10)
    axis.set_xticks([index - 0.5 for index in range(length + 1)], minor=True)
    axis.set_yticks([index - 0.5 for index in range(length + 1)], minor=True)
    axis.grid(which="minor", color="#faf9f6", linewidth=1)
    axis.tick_params(which="minor", length=0)
    colorbar = figure.colorbar(displayed, ax=axis, fraction=0.045, pad=0.035)
    colorbar.set_label("Attention probability (absolute scale)")
    colorbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
    axis.set_title("Measured in eval mode. Future positions have weight zero.\nA weight describes value mixing, not a complete explanation of a prediction.", y=-0.18, fontsize=9)
    return _save(figure, path)
