from __future__ import annotations

import ast
import csv
import math
import re
from pathlib import Path
from typing import Any

import numpy as np


_NAME_RE = re.compile(r"[^0-9a-zA-Z_]")


def matlab_name(name: str) -> str:
    cleaned = _NAME_RE.sub("_", name.strip())
    if not cleaned:
        return "unnamed"
    if cleaned[0].isdigit():
        cleaned = f"x{cleaned}"
    return cleaned


def load_data(filename: str | Path) -> dict[str, Any]:
    """Load the CSV parameter files used by the MATLAB scripts."""
    path = Path(filename)
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    data: dict[str, Any] = {}
    for row in rows:
        raw_name = (row.get("name") or "").strip()
        if not raw_name:
            continue
        data[matlab_name(raw_name)] = parse_value(row.get("value", ""))
    return data


def parse_value(raw: Any) -> Any:
    if raw is None:
        return None
    if isinstance(raw, (int, float, np.number)):
        return raw

    text = str(raw).strip()
    if not text:
        return np.array([])
    if text == "[]":
        return np.array([])
    if (text.startswith("'") and text.endswith("'")) or (
        text.startswith('"') and text.endswith('"')
    ):
        return text[1:-1]

    linspace_match = re.fullmatch(r"linspace\((.*)\)", text)
    if linspace_match:
        args = [parse_value(part) for part in linspace_match.group(1).split(",")]
        if len(args) != 3:
            raise ValueError(f"linspace expects 3 arguments: {text}")
        return np.linspace(float(args[0]), float(args[1]), int(args[2]))

    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return np.array([])
        if ";" in inner:
            rows = [
                [parse_value(token) for token in re.split(r"[\s,]+", row.strip()) if token]
                for row in inner.split(";")
            ]
            return np.array(rows, dtype=float)
        tokens = [parse_value(token) for token in re.split(r"[\s,]+", inner) if token]
        return np.array(tokens, dtype=float)

    if ":" in text and re.fullmatch(r"[-+0-9.eE:\s]+", text):
        parts = [float(part) for part in text.split(":")]
        if len(parts) == 2:
            start, stop = parts
            step = 1.0
        elif len(parts) == 3:
            start, step, stop = parts
        else:
            raise ValueError(f"Unsupported MATLAB range: {text}")
        count = int(math.floor((stop - start) / step + 1e-12)) + 1
        return start + step * np.arange(count)

    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass

    try:
        return float(eval(text, {"__builtins__": {}}, {"pi": math.pi, "np": np, "sqrt": np.sqrt}))
    except Exception:
        return text


def time_vector(tspan: Any, default_points: int = 1000) -> np.ndarray:
    values = np.asarray(tspan, dtype=float).ravel()
    if values.size == 2:
        return np.linspace(values[0], values[1], default_points)
    return values


def show_plots() -> None:
    import matplotlib.pyplot as plt

    plt.tight_layout()
    plt.show()
