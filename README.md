# Blueprint Assembly — FreeCAD Python Macro

A procedurally generated 3D model recreating an exploded technical assembly diagram, built entirely from a single Python script run inside FreeCAD.

---

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

## How to Run

1. Open FreeCAD
2. Go to **Tools → Macro → Macros...**
3. Click **Create** or **Open** and load `blueprint_assembly.py`
4. Click **Execute**

The script will generate all objects, recompute the document, and fit the isometric view automatically.

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