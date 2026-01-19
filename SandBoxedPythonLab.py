#!/usr/bin/env python
import sys
import json
import traceback
import math
import random
import io
import base64
from pathlib import Path
from typing import Any, Dict, List, Optional

# =========================
# Configuration
# =========================

SANDBOX_ROOT = Path(__file__).parent / "sandbox"
SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)

# GPU backend flags
GPU_BACKEND = None
xp = None  # will be set to numpy / cupy / torch-like

# =========================
# Safe imports (curated whitelist)
# =========================

# Core numeric stack
try:
    import numpy as np
except ImportError:
    np = None

try:
    import scipy
    from scipy import integrate
except ImportError:
    scipy = None
    integrate = None

# Plotting (headless)
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib = None
    plt = None

# GPU backends (auto-detect)
try:
    import cupy as cp
    GPU_BACKEND = "cupy"
    xp = cp
except Exception:
    cp = None

if GPU_BACKEND is None:
    try:
        import torch
        GPU_BACKEND = "torch"
        xp = torch
    except Exception:
        torch = None

# Fallback to numpy if no GPU backend
if xp is None:
    xp = np
    GPU_BACKEND = "cpu"


# =========================
# Utility: JSON-RPC I/O
# =========================

def read_message() -> Optional[Dict[str, Any]]:
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def send_message(msg: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


# =========================
# Sandbox utilities
# =========================

def sandbox_path(rel: str) -> Path:
    rel = rel.replace("..", "")
    return SANDBOX_ROOT / rel


def reset_sandbox_dir() -> None:
    if SANDBOX_ROOT.exists():
        for p in SANDBOX_ROOT.glob("**/*"):
            if p.is_file():
                try:
                    p.unlink()
                except Exception:
                    pass


# =========================
# Physics helpers (Kerr-ish, simplified)
# =========================

def kerr_isco_radius(a: float) -> float:
    """
    Approximate ISCO radius (prograde) in units of GM/c^2 for spin a in [0, 1).
    """
    z1 = 1 + (1 - a**2) ** (1/3) * ((1 + a) ** (1/3) + (1 - a) ** (1/3))
    z2 = (3 * a**2 + z1**2) ** 0.5
    return 3 + z2 - ((3 - z1) * (3 + z1 + 2 * z2)) ** 0.5


def gravitational_redshift(r: float, m: float = 1.0) -> float:
    """
    Very rough Schwarzschild redshift factor at radius r (in units of GM/c^2).
    """
    rs = 2 * m
    if r <= rs:
        return float("inf")
    return 1.0 / math.sqrt(1 - rs / r)


def sample_orbit_radii(a: float, n: int = 128) -> List[float]:
    """
    Sample radii from ISCO outward for simple orbit visualizations.
    """
    r_isco = kerr_isco_radius(a)
    return [r_isco + (i / (n - 1)) * (20 - r_isco) for i in range(n)]


# =========================
# Chaos parameter generator
# =========================

def generate_chaos_parameters() -> Dict[str, Any]:
    """
    Generate a chaotic but bounded parameter set for a near-extremal Kerr BH.
    """
    spin = random.uniform(0.9, 0.9999)
    turbulence = random.uniform(0.3, 1.5)
    hotspot_orbits = random.randint(1, 7)
    lensing_intensity = random.uniform(0.8, 1.4)
    frame_drag_factor = random.uniform(1.0, 1.5)
    noise_seed = random.randint(0, 10_000_000)

    return {
        "spin": spin,
        "turbulence": turbulence,
        "hotspot_orbits": hotspot_orbits,
        "lensing_intensity": lensing_intensity,
        "frame_drag_factor": frame_drag_factor,
        "noise_seed": noise_seed,
    }


# =========================
# Noise / field generation
# =========================

def generate_noise_field(width: int, height: int, seed: Optional[int] = None) -> List[List[float]]:
    if np is None:
        raise RuntimeError("NumPy is required for noise generation.")
    if seed is not None:
        np.random.seed(seed)
    field = np.random.rand(height, width).astype("float32")
    return field.tolist()


# =========================
# Plotting helpers
# =========================

def plot_data_series(x: List[float], y: List[float], title: str = "Plot") -> bytes:
    if plt is None:
        raise RuntimeError("matplotlib is not available for plotting.")
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# =========================
# Sandboxed Python execution
# =========================

ALLOWED_MODULES = {
    "math": math,
    "random": random,
    "json": json,
}

if np is not None:
    ALLOWED_MODULES["numpy"] = np
    ALLOWED_MODULES["np"] = np

if scipy is not None:
    ALLOWED_MODULES["scipy"] = scipy
if integrate is not None:
    ALLOWED_MODULES["integrate"] = integrate

if matplotlib is not None and plt is not None:
    ALLOWED_MODULES["matplotlib"] = matplotlib
    ALLOWED_MODULES["plt"] = plt

if cp is not None:
    ALLOWED_MODULES["cupy"] = cp
if 'torch' in globals() and torch is not None:
    ALLOWED_MODULES["torch"] = torch

# Expose our own helpers
ALLOWED_MODULES["kerr_isco_radius"] = kerr_isco_radius
ALLOWED_MODULES["gravitational_redshift"] = gravitational_redshift
ALLOWED_MODULES["sample_orbit_radii"] = sample_orbit_radii
ALLOWED_MODULES["generate_chaos_parameters"] = generate_chaos_parameters
ALLOWED_MODULES["generate_noise_field"] = generate_noise_field


def run_sandboxed_python(code: str) -> Dict[str, Any]:
    """
    Execute Python code in a restricted environment.
    Returns stdout, stderr, and optionally a 'result' variable if defined.
    """
    # Restricted builtins
    safe_builtins = {
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
        "print": print,
    }

    # Globals for exec
    env_globals = {
        "__builtins__": safe_builtins,
    }
    env_globals.update(ALLOWED_MODULES)

    # Locals
    env_locals: Dict[str, Any] = {}

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    # Redirect stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stdout_buf
    sys.stderr = stderr_buf

    try:
        exec(code, env_globals, env_locals)
    except Exception:
        traceback.print_exc(file=stderr_buf)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    result = env_locals.get("result", None)

    return {
        "stdout": stdout_buf.getvalue(),
        "stderr": stderr_buf.getvalue(),
        "result": result,
    }


# =========================
# File sandbox tools
# =========================

def tool_write_file(params: Dict[str, Any]) -> Dict[str, Any]:
    rel_path = params.get("path")
    content = params.get("content", "")
    if not isinstance(rel_path, str):
        raise ValueError("path must be a string")
    p = sandbox_path(rel_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return {"ok": True}


def tool_read_file(params: Dict[str, Any]) -> Dict[str, Any]:
    rel_path = params.get("path")
    if not isinstance(rel_path, str):
        raise ValueError("path must be a string")
    p = sandbox_path(rel_path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {rel_path}")
    content = p.read_text(encoding="utf-8")
    return {"content": content}


def tool_list_files(params: Dict[str, Any]) -> Dict[str, Any]:
    files = []
    for p in SANDBOX_ROOT.glob("**/*"):
        if p.is_file():
            rel = p.relative_to(SANDBOX_ROOT).as_posix()
            files.append(rel)
    return {"files": files}


def tool_reset_sandbox(params: Dict[str, Any]) -> Dict[str, Any]:
    reset_sandbox_dir()
    return {"ok": True}


# =========================
# Tool implementations
# =========================

def tool_run_python(params: Dict[str, Any]) -> Dict[str, Any]:
    # Accept both "code" and "python"
    code = params.get("code") or params.get("python") or ""
    if not isinstance(code, str):
        raise ValueError("code must be a string")

    return run_sandboxed_python(code)


def tool_simulate_kerr(params: Dict[str, Any]) -> Dict[str, Any]:
    a = float(params.get("spin", 0.95))
    n = int(params.get("samples", 128))
    radii = sample_orbit_radii(a, n)
    redshifts = [gravitational_redshift(r) for r in radii]
    return {
        "spin": a,
        "radii": radii,
        "redshifts": redshifts,
    }


def tool_generate_noise(params: Dict[str, Any]) -> Dict[str, Any]:
    width = int(params.get("width", 64))
    height = int(params.get("height", 64))
    seed = params.get("seed", None)
    if seed is not None:
        seed = int(seed)
    field = generate_noise_field(width, height, seed)
    return {
        "width": width,
        "height": height,
        "field": field,
    }


def tool_plot_data(params: Dict[str, Any]) -> Dict[str, Any]:
    x = params.get("x", [])
    y = params.get("y", [])
    title = params.get("title", "Plot")
    if not isinstance(x, list) or not isinstance(y, list):
        raise ValueError("x and y must be lists of numbers")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    x_f = [float(v) for v in x]
    y_f = [float(v) for v in y]
    png_bytes = plot_data_series(x_f, y_f, title)
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return {
        "image_base64": b64,
        "format": "png",
    }


def tool_chaos_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    return generate_chaos_parameters()


def tool_gpu_info(params: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "backend": GPU_BACKEND,
        "has_cupy": cp is not None,
        "has_torch": ('torch' in globals() and torch is not None),
    }


TOOLS = {
    "run_python": tool_run_python,
    "simulate_kerr": tool_simulate_kerr,
    "generate_noise": tool_generate_noise,
    "plot_data": tool_plot_data,
    "chaos_parameters": tool_chaos_parameters,
    "write_file": tool_write_file,
    "read_file": tool_read_file,
    "list_files": tool_list_files,
    "reset_sandbox": tool_reset_sandbox,
    "gpu_info": tool_gpu_info,
}


# =========================
# MCP-like protocol
# =========================

def handle_list_tools(request_id: Any) -> None:
    tools_desc = []
    for name in TOOLS.keys():
        tools_desc.append({
            "name": name,
            "description": f"Tool: {name}",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": True,
            },
        })
    send_message({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": tools_desc
        }
    })


def handle_call_tool(request_id: Any, params: Dict[str, Any]) -> None:
    name = params.get("name")
    arguments = params.get("arguments", {})
    if name not in TOOLS:
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Unknown tool: {name}"
            }
        })
        return
    try:
        result = TOOLS[name](arguments)
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        })
    except Exception as e:
        send_message({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": f"Tool error: {str(e)}",
                "data": traceback.format_exc()
            }
        })


def handle_initialize(request_id, params):
    send_message({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "python-lab",
                "version": "1.0.0"
            },
            "capabilities": {
                "tools": {}   # MUST be an object
            }
        }
    })



def main_loop() -> None:
    while True:
        msg = read_message()
        if msg is None:
            break

        msg_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params", {}) or {}

        if method == "initialize":
            handle_initialize(msg_id, params)
        elif method in ("list_tools", "tools/list"):
            handle_list_tools(msg_id)
        elif method in ("call_tool", "tools/call"):
            handle_call_tool(msg_id, params)
        else:
            send_message({
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Unknown method: {method}"
        }
    })




if __name__ == "__main__":
    main_loop()
