"""
Blueprint Assembly - FreeCAD Python Script
===========================================
Recreates the exploded assembly diagram from the blueprint image.
Run this inside FreeCAD via: Tfreools > Macros > Run Macro
Or from CLI: freecadcmd blueprint_assembly.py

Components modelled (rough geometry / placeholder shapes):
  TOP HOUSING
    - Electrostatic-sensing illuminated ABS skin (outer cube shell)
    - Steel & fiber reinforced concrete shell (mid cube)
    - MIL-A-12560 Ballistic Steel Lining (inner cube)
  ELECTRONICS STACK (PCB slabs)
    - Ethernet Shield x2
    - Intel Compute Stick
    - Taidecent
    - Teensy x3
    - Fiber-optic Ethernet Converter / Faraday Cage box
    - KDU (small block)
    - Internal Sensor Pack
    - IDU
  CONNECTIVITY (on a side bracket)
    - Starlink dish (cylinder + dish)
    - Data Cable / Cellular / LoRa (small boxes)
  POWER STACK
    - 6x 5V LiIon Battery Pack (box)
    - AC-DC Converter (box)
    - SPDT Power Isolation Relays (box)
  CONSOLE (monitor + keyboard)
  BASE
    - MIL-A-12560 Ballistic Steel Base (plate)
    - Concrete Base (plate)
    - 4x Cantilever Load Cells (small blocks at corners)
    - 4x Steel Legs (cylinders)
"""

import FreeCAD as App
import Part
import math

doc = App.newDocument("BlueprintAssembly")


# ── helpers ──────────────────────────────────────────────────────────────────

def box(name, x, y, z, lx, ly, lz, color=(0.6, 0.6, 0.6)):
    """Create a solid box. Origin at centre-bottom of the box."""
    sh = Part.makeBox(lx, ly, lz, App.Vector(x - lx/2, y - ly/2, z))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = sh
    obj.ViewObject.ShapeColor = color
    return obj


def hollow_box(name, x, y, z, lx, ly, lz, wall, color=(0.5, 0.5, 0.5)):
    """Hollow cube shell (outer - inner)."""
    outer = Part.makeBox(lx, ly, lz, App.Vector(x - lx/2, y - ly/2, z))
    inner = Part.makeBox(
        lx - 2*wall, ly - 2*wall, lz - 2*wall,
        App.Vector(x - lx/2 + wall, y - ly/2 + wall, z + wall)
    )
    sh = outer.cut(inner)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = sh
    obj.ViewObject.ShapeColor = color
    return obj


def cylinder(name, x, y, z, r, h, color=(0.5, 0.5, 0.5)):
    sh = Part.makeCylinder(r, h, App.Vector(x, y, z))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = sh
    obj.ViewObject.ShapeColor = color
    return obj


def thin_slab(name, x, y, z, lx, ly, thickness=2, color=(0.2, 0.8, 0.2)):
    return box(name, x, y, z, lx, ly, thickness, color)


# ── coordinate layout (Z grows upward, all units mm) ─────────────────────────
# We lay out the exploded view vertically, matching the blueprint's top-to-bottom
# stacking order.

CX = 0    # centre X
CY = 0    # centre Y

# ── BASE ─────────────────────────────────────────────────────────────────────
Z = 0

# Steel Legs (4 cylinders at corners)
LEG_R = 15
LEG_H = 80
OFFSET = 120
for lx, ly in [(-OFFSET, -OFFSET), (OFFSET, -OFFSET),
                (-OFFSET,  OFFSET), (OFFSET,  OFFSET)]:
    cylinder(f"SteelLeg_{lx}_{ly}", lx, ly, Z, LEG_R, LEG_H, color=(0.55, 0.55, 0.6))

Z += LEG_H

# Concrete Base
CONCRETE_H = 30
box("ConcreteBase", CX, CY, Z, 340, 340, CONCRETE_H, color=(0.6, 0.58, 0.54))
Z += CONCRETE_H

# 4x Cantilever Load Cells (corner blocks, on top of concrete)
for lx, ly in [(-130, -130), (130, -130), (-130, 130), (130, 130)]:
    box(f"LoadCell_{lx}_{ly}", lx, ly, Z, 30, 20, 15, color=(0.8, 0.6, 0.2))

# MIL-A-12560 Ballistic Steel Base
STEEL_BASE_H = 20
box("BallisticSteelBase", CX, CY, Z, 340, 340, STEEL_BASE_H, color=(0.35, 0.35, 0.4))
Z += STEEL_BASE_H

# ── GAP (power stack sits above base) ────────────────────────────────────────
Z += 40   # visual explode gap

# ── POWER STACK ──────────────────────────────────────────────────────────────

# SPDT Power Isolation Relays
RELAY_H = 25
box("SPDT_PowerRelays", CX, CY, Z, 120, 80, RELAY_H, color=(0.3, 0.5, 0.8))
Z += RELAY_H + 15

# AC-DC Converter
ACDC_H = 35
box("ACDC_Converter", CX, CY, Z, 100, 70, ACDC_H, color=(0.7, 0.7, 0.3))
Z += ACDC_H + 15

# 6x LiIon Battery Pack
BAT_H = 40
box("LiIon_BatteryPack", CX, CY, Z, 140, 90, BAT_H, color=(0.2, 0.7, 0.3))
Z += BAT_H

# ── GAP ──────────────────────────────────────────────────────────────────────
Z += 50

# ── ELECTRONICS STACK ────────────────────────────────────────────────────────

# IDU
thin_slab("IDU", CX, CY, Z, 100, 60, 8, color=(0.3, 0.8, 0.5))
Z += 12

# Internal Sensor Pack
thin_slab("InternalSensorPack", CX, CY, Z, 80, 50, 8, color=(0.5, 0.7, 0.9))
Z += 12

# KDU (small block)
box("KDU", CX - 80, CY, Z, 30, 20, 10, color=(0.9, 0.5, 0.2))
Z += 14

# Fiber-optic Ethernet Converter / Faraday Cage
FARADAY_H = 40
box("FiberOptic_FaradayCage", CX, CY, Z, 110, 80, FARADAY_H, color=(0.6, 0.3, 0.8))
Z += FARADAY_H + 10

# Teensy.002
thin_slab("Teensy_002", CX, CY, Z, 55, 18, 4, color=(0.1, 0.6, 0.9))
Z += 8
# Teensy
thin_slab("Teensy", CX, CY, Z, 55, 18, 4, color=(0.1, 0.6, 0.9))
Z += 8
# Teensy.001
thin_slab("Teensy_001", CX, CY, Z, 55, 18, 4, color=(0.1, 0.6, 0.9))
Z += 8

# Taidecent
thin_slab("Taidecent", CX, CY, Z, 70, 30, 5, color=(0.9, 0.4, 0.4))
Z += 9

# Intel Compute Stick
box("IntelComputeStick", CX, CY, Z, 110, 38, 12, color=(0.2, 0.4, 0.8))
Z += 16

# Ethernet Shield.001
thin_slab("EthernetShield_001", CX, CY, Z, 85, 55, 6, color=(0.2, 0.7, 0.2))
Z += 10

# Ethernet Shield
thin_slab("EthernetShield", CX, CY, Z, 85, 55, 6, color=(0.2, 0.7, 0.2))
Z += 10

# ── GAP ──────────────────────────────────────────────────────────────────────
Z += 60

# ── TOP HOUSING (3-layer cube) ────────────────────────────────────────────────

# MIL-A-12560 Ballistic Steel Lining (innermost)
BSL_SIZE = 220
BSL_H    = 220
BSL_WALL = 12
hollow_box("BallisticSteelLining", CX, CY, Z, BSL_SIZE, BSL_SIZE, BSL_H,
           BSL_WALL, color=(0.35, 0.35, 0.45))
Z += BSL_H + 10

# Steel & Fiber Reinforced Concrete Shell (mid)
CONC_SIZE = 260
CONC_H    = 40
CONC_WALL = 15
hollow_box("ConcreteShell", CX, CY, Z, CONC_SIZE, CONC_SIZE, CONC_H,
           CONC_WALL, color=(0.55, 0.52, 0.48))
Z += CONC_H + 10

# Electrostatic-sensing ABS Skin (outermost)
ABS_SIZE = 300
ABS_H    = 30
ABS_WALL = 5
hollow_box("ABS_Skin", CX, CY, Z, ABS_SIZE, ABS_SIZE, ABS_H,
           ABS_WALL, color=(0.85, 0.85, 0.9))

# ── CONNECTIVITY (offset to the right, mid-height) ──────────────────────────
# Place connectivity cluster at the electronics mid-level

CONN_Z = 400   # roughly mid-assembly height
CONN_X = 320   # to the right

# Starlink dish: cylinder base + hemisphere stand
cylinder("Starlink_Mast",  CONN_X, CY, CONN_Z,      8, 80, color=(0.8, 0.8, 0.8))
cylinder("Starlink_Dish",  CONN_X, CY, CONN_Z + 80, 55,  5, color=(0.7, 0.7, 0.9))

# LoRa module
box("LoRa",           CONN_X, CY + 80,  CONN_Z, 40, 25, 15, color=(0.9, 0.5, 0.1))
# Cellular Data
box("CellularData",   CONN_X, CY + 40,  CONN_Z, 40, 25, 12, color=(0.3, 0.8, 0.5))
# Data Cable endpoint
box("DataCable_End",  CONN_X, CY,       CONN_Z, 20, 15, 10, color=(0.6, 0.3, 0.2))

# ── CONSOLE (offset to the right, lower) ─────────────────────────────────────
CONS_Z = 250
CONS_X = 320

# Monitor (box with thin bezel)
box("Console_Monitor",  CONS_X, CY, CONS_Z,        180, 20, 130, color=(0.15, 0.15, 0.15))
# Screen face (slightly inset bright slab)
box("Console_Screen",   CONS_X, CY + 2, CONS_Z + 10, 160, 5, 110, color=(0.3, 0.6, 0.9))
# Keyboard
box("Console_Keyboard", CONS_X, CY - 60, CONS_Z,    160, 50, 10, color=(0.2, 0.2, 0.2))

# ── FINALISE ─────────────────────────────────────────────────────────────────
doc.recompute()
App.Console.PrintMessage("Blueprint assembly created successfully.\n")
App.Console.PrintMessage(f"Total objects: {len(doc.Objects)}\n")

# Optional: export to STEP for use in other CAD tools
try:
    import ImportGui
    out_path = "/mnt/user-data/outputs/blueprint_assembly.step"
    ImportGui.export(doc.Objects, out_path)
    App.Console.PrintMessage(f"Exported STEP: {out_path}\n")
except Exception as e:
    App.Console.PrintMessage(f"STEP export skipped ({e})\n")