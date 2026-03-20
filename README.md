# Blueprint Assembly for Epitrope — FreeCAD Python Macro

A fully procedural 3D assembly that recreates an exploded technical blueprint, generated entirely from a single Python script executed inside FreeCAD.

---
<img width="744" height="1052" alt="image" src="https://github.com/user-attachments/assets/924a0658-cd62-474b-a1c2-9e5ae3cbfe4b" />

<img width="1470" height="956" alt="Screenshot 2026-03-19 at 9 31 44 PM" src="https://github.com/user-attachments/assets/2abf97bc-17ae-4ca9-8d7d-529404539e67" />


## What It Models

The assembly is based on a multi-layer exploded blueprint and covers 24 component groups across four sections:

**Top Shell (exploded cube)**
- Electrostatic-sensing illuminated ABS skin (outermost)
- Steel & fiber reinforced concrete shell (middle)
- MIL-A-12560 Ballistic Steel Lining (innermost)

**Electronics Stack**
- Ethernet Shield ×2, Intel Compute Stick, Taidecent module
- Teensy ×3, Fiber-optic Ethernet Converter
- Faraday Cage (>100dB @ 1GHz), KDU, Internal Sensor Pack, IDU

**Connectivity Cluster**
- Starlink dish (primary + sub-reflector + mast)
- LoRa, Cellular Data Connection, Data Cable terminator
- Console / CRT monitor with stand and keyboard

### Power Section

* 6× 5V Li-Ion battery packs (cylindrical cells)
* AC-DC converter with heat sink fins
* SPDT power isolation relays ×2

### Base

* Ballistic steel base plate
* Concrete base layer
* 4× cantilever load cells
* 4× steel support legs

---

## Requirements

* FreeCAD 0.20 or newer
* No external dependencies

This project uses only:

* `FreeCAD`
* `Part`

---

## Quick Start

```bash
git clone https://github.com/your-repo/Freecadproject.git
cd Freecadproject
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD blueprint_assembly_part2.py
```

---

## Setup Notes

This is **not a standard Python project**.

* No `pip install`
* No `requirements.txt`
* No virtual environments

The script must run using FreeCAD’s bundled Python interpreter.

### macOS Default Path

```
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD
```

### Important

❌ This will NOT work:

```bash
python3 blueprint_assembly_part2.py
```

✅ This WILL work:

```bash
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD blueprint_assembly_part2.py
```

### Custom Install Path

If FreeCAD is installed elsewhere, replace the path:

```bash
/path/to/FreeCAD blueprint_assembly_part2.py
```

### Optional Shortcut

```bash
ln -s /Applications/FreeCAD.app/Contents/MacOS/FreeCAD /usr/local/bin/freecad
```

Then run:

```bash
freecad blueprint_assembly_part2.py
```

---
📥 1. Clone the Project

Open terminal (inside VS Code or normal terminal):

git clone https://github.com/your-repo/Freecadproject.git
cd Freecadproject

Then open it in VS Code:

code .
📦 2. Install / Setup

No Python packages needed — this script uses FreeCAD’s built-in Python environment.

Just make sure:

FreeCAD is installed in /Applications/FreeCAD.app (Mac)

Or adjust path if different

▶️ 3. Run the Script (3 Options)
✅ Option A — Easiest (Recommended)

Open FreeCAD GUI:

Launch FreeCAD

Go to:

Tools → Macro → Execute Macro

Select:

blueprint_assembly_part2.py

✔️ This is the most stable method

⚡ Option B — Run from VS Code Terminal

Inside your project folder:

/Applications/FreeCAD.app/Contents/MacOS/FreeCAD blueprint_assembly_part2.py

✔️ This is what your logs show — and it works

You should see:

Blueprint Assembly — generation complete!
Objects created : 144
🧠 Option C — Headless (advanced)
/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd blueprint_assembly_part2.py

Runs without full GUI (faster, but no visual preview).
---

## Color Guide

| Color     | Components                         |
| --------- | ---------------------------------- |
| Magenta   | ABS skin, load cells, steel legs   |
| Green     | Concrete layers, Ethernet shields  |
| Cyan      | Ballistic steel, electronics stack |
| Red       | Connectivity cluster               |
| Orange    | Power components                   |
| Yellow    | PCB modules                        |
| Silver    | Metal hardware, connectors         |
| Dark Gray | Faraday cage, display bezels       |

---

## Exporting

Use **File → Export** and choose:

* **STEP (.step)** — CAD workflows
* **OBJ (.obj)** — rendering / game engines
* **STL (.stl)** — 3D printing

---

## Tips

* Use **Shaded mode** for solid visualization
* Use **Wireframe mode** to inspect internal layers
* Press **Space** on objects to toggle visibility
* Each subsystem is spatially separated for easy isolation and rendering

---

## Project Files

| File | Description |
|------|-------------|
| `blueprint_assembly_part2.py` |
| `blueprint_assembly_part1.py` |
| `README.md` | This file |
