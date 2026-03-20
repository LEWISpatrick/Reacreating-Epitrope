# Blueprint Assembly for Epitrope — FreeCAD Python Macro

A procedurally generated 3D model recreating an exploded technical assembly diagram, built entirely from a single Python script run inside FreeCAD.

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

**Power Section**
- 6× 5V LiIon Battery Pack (cylindrical cells in tray)
- AC-DC Converter with heat-sink fins
- SPDT Power Isolation Relays ×2

**Base**
- MIL-A-12560 Ballistic Steel Base
- Concrete Base
- 4× Cantilever Load Cells
- 4× Steel Legs

---

## Requirements

- [FreeCAD](https://www.freecad.org/) 0.20 or later
- No additional Python packages — uses only the built-in `FreeCAD` and `Part` modules

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

## Colour Guide

| Colour | Components |
|--------|-----------|
| Magenta | ABS skin, load cells, steel legs |
| Green | Concrete layers, Ethernet shields |
| Cyan | Ballistic steel, electronics stack |
| Red | Connectivity cluster (Starlink, LoRa, console) |
| Orange | Power components (batteries, converter, relays) |
| Yellow | PCB modules (Teensy, Taidecent, converter) |
| Silver | Metal hardware, connectors, masts |
| Dark Gray | Faraday cage, screen bezels |

---

## Exporting for Rendering

Once generated, export via **File → Export** and choose your format:

- **STEP (.step)** — best for CAD tools and Fusion 360
- **OBJ (.obj)** — best for Blender, KeyShot, or game engines
- **STL (.stl)** — best for 3D printing prep

---

## Tips

- **View → Draw Style → Shaded** for solid rendering
- **View → Draw Style → Wireframe** to inspect hollow shell layers
- Press **Space** on any object in the Model tree to toggle visibility
- The electronics stack, power section, and connectivity cluster are each spatially separated, making it easy to isolate sections for individual renders

---

## File

| File | Description |
|------|-------------|
| `blueprint_assembly_part2.py` |
| `blueprint_assembly_part1.py` |
| `README.md` | This file |
