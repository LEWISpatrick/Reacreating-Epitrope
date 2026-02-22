"""
Blueprint Assembly - FreeCAD Python Script
==========================================
Recreates the exploded assembly diagram from the blueprint image.
Run this script inside FreeCAD via: Tools > Macro > Execute Macro

Components (top to bottom, matching the blueprint):

  TOP SHELL (exploded cube)
    1.  Electrostatic-sensing illuminated ABS skin       (outermost cube shell)
    2.  Steel & fiber reinforced concrete shell           (middle cube shell)
    3.  MIL-A-12560 Ballistic Steel Lining               (innermost cube shell)

  ELECTRONICS STACK (centre column)
    4.  Ethernet Shield x2                               (thin green PCBs)
    5.  Intel Compute Stick                              (silver stick)
    6.  Taidecent module                                 (small yellow box)
    7.  Teensy x3                                        (tiny yellow boards)
    8.  Fiber-optic Ethernet Converter                   (yellow module)
    9.  Faraday Cage  (>100dB @ 1GHz)                   (dark wire-frame box)
    10. KDU unit                                         (cyan box)
    11. Internal Sensor Pack                             (flat slab)
    12. IDU unit                                         (thin slab)

  CONNECTIVITY CLUSTER (right side)
    13. Starlink dish                                    (cone + mast)
    14. LoRa antenna module                              (red box + antenna)
    15. Cellular Data Connection module                  (red box)
    16. Data Cable terminator                            (red box)
    17. Console / monitor                                (box + screen bezel)

  POWER SECTION (centre column, below electronics)
    18. 6x 5V LiIon Battery Pack                        (6 cells in tray)
    19. AC-DC Converter                                  (finned orange box)
    20. SPDT Power Isolation Relays                      (two relay blocks)

  BASE SECTION
    21. MIL-A-12560 Ballistic Steel Base                 (heavy cyan plate)
    22. Concrete Base                                    (thick green slab)
    23. 4x Cantilever Load Cells                         (corner beams)
    24. Steel Legs x4                                    (cylinders at corners)

All dimensions in mm.  Y-axis = vertical (up).
"""

import FreeCAD as App
import Part
import math

doc = App.newDocument("BlueprintAssembly")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def make_box(name, w, h, d, pos, color=(0.8, 0.8, 0.8), transparency=0):
    obj = doc.addObject("Part::Box", name)
    obj.Width  = w
    obj.Height = h
    obj.Length = d
    obj.Placement = App.Placement(App.Vector(*pos), App.Rotation())
    obj.ViewObject.ShapeColor  = color
    obj.ViewObject.Transparency = transparency
    return obj


def make_cylinder(name, r, h, pos, color=(0.7, 0.7, 0.7)):
    obj = doc.addObject("Part::Cylinder", name)
    obj.Radius = r
    obj.Height = h
    obj.Placement = App.Placement(App.Vector(*pos), App.Rotation())
    obj.ViewObject.ShapeColor = color
    return obj


def make_cone(name, r1, r2, h, pos, color=(0.7, 0.7, 0.7)):
    obj = doc.addObject("Part::Cone", name)
    obj.Radius1 = r1
    obj.Radius2 = r2
    obj.Height  = h
    obj.Placement = App.Placement(App.Vector(*pos), App.Rotation())
    obj.ViewObject.ShapeColor = color
    return obj


def hollow_shell(name, ow, oh, od, wall, pos, color, transparency=25):
    """
    Build a hollow open-top shell as a Part::Feature compound of 5 face slabs
    (bottom + 4 sides). Avoids slow boolean cuts.
    """
    x0, y0, z0 = pos
    t = wall
    slabs = [
        Part.makeBox(ow, t,  od,  App.Vector(x0,        y0,        z0)),         # bottom
        Part.makeBox(ow, oh, t,   App.Vector(x0,        y0,        z0)),          # front
        Part.makeBox(ow, oh, t,   App.Vector(x0,        y0,        z0 + od - t)), # back
        Part.makeBox(t,  oh, od,  App.Vector(x0,        y0,        z0)),          # left
        Part.makeBox(t,  oh, od,  App.Vector(x0 + ow - t, y0,      z0)),          # right
    ]
    compound = Part.makeCompound(slabs)
    feat = doc.addObject("Part::Feature", name)
    feat.Shape = compound
    feat.ViewObject.ShapeColor   = color
    feat.ViewObject.Transparency = transparency
    return feat


# ---------------------------------------------------------------------------
# Colour palette  (R, G, B)  0–1 float
# ---------------------------------------------------------------------------
MAGENTA  = (1.00, 0.20, 0.80)
GREEN    = (0.10, 0.85, 0.35)
CYAN     = (0.10, 0.85, 1.00)
RED      = (1.00, 0.20, 0.20)
ORANGE   = (1.00, 0.55, 0.05)
YELLOW   = (0.90, 0.90, 0.05)
SILVER   = (0.75, 0.75, 0.82)
DKGRAY   = (0.25, 0.28, 0.30)

# ==========================================================================
# BASE SECTION   Y = 0 … ~165
# ==========================================================================

LEG_R, LEG_H = 18, 80
for lx, lz in [(-150, -150), (150, -150), (-150, 150), (150, 150)]:
    make_cylinder(f"SteelLeg_x{lx}_z{lz}", LEG_R, LEG_H,
                  (lx - LEG_R, 0, lz - LEG_R), MAGENTA)

# Cantilever load cells — flat rectangular beams on top of legs
LC_W, LC_H, LC_D = 70, 18, 130
for cx, cz in [(-150, -150), (150, -150), (-150, 150), (150, 150)]:
    make_box(f"LoadCell_x{cx}_z{cz}", LC_W, LC_H, LC_D,
             (cx - LC_W / 2, LEG_H, cz - LC_D / 2), MAGENTA)

CONC_Y = LEG_H + LC_H
make_box("ConcreteBase", 360, 45, 360, (-180, CONC_Y, -180), GREEN)

STEEL_BASE_Y = CONC_Y + 45
make_box("BallisticSteelBase", 310, 28, 310, (-155, STEEL_BASE_Y, -155), CYAN)

BASE_TOP = STEEL_BASE_Y + 28

# ==========================================================================
# POWER SECTION   Y = BASE_TOP + 20 … ~460
# ==========================================================================

PW_Y = BASE_TOP + 25

# SPDT Relays — two blocks with coil detail
make_box("SPDTRelay_A", 65, 38, 50, (-75, PW_Y, -25), ORANGE)
make_box("SPDTRelay_B", 65, 38, 50, ( 10, PW_Y, -25), ORANGE)
make_cylinder("RelayCoil_A",  9, 22, (-45, PW_Y + 38,  0), SILVER)
make_cylinder("RelayCoil_B",  9, 22, ( 40, PW_Y + 38,  0), SILVER)
# Terminal pins
for ti, tx in enumerate([-65, -45, -25, 10, 30, 50]):
    make_cylinder(f"RelayPin_{ti}", 2, 10, (tx, PW_Y - 10, -5), SILVER)

RELAY_TOP = PW_Y + 38

# AC-DC Converter — box with heat-sink fins
ACDC_Y = RELAY_TOP + 20
make_box("ACDC_Converter_Body", 130, 55, 90, (-65, ACDC_Y, -45), ORANGE)
for fi in range(7):
    make_box(f"ACDCFin_{fi}", 130, 10, 5,
             (-65, ACDC_Y + 55, -45 + fi * 12), SILVER)
# AC input terminals
make_box("ACDC_InputTerminal", 20, 20, 15, (-75, ACDC_Y + 15, 45), DKGRAY)

ACDC_TOP = ACDC_Y + 55 + 10   # top of fins

# 6x 5V LiIon Battery Pack — 2 rows × 3 cells
CELL_R, CELL_H = 19, 68
BATT_Y = ACDC_TOP + 25
BATT_TRAY_Z = -35
cell_pos = [
    (-58, -25), (-58, 0), (-58, 25),
    (  8, -25), (  8, 0), (  8, 25),
]
for i, (bx, bz) in enumerate(cell_pos):
    make_cylinder(f"BattCell_{i}", CELL_R, CELL_H, (bx, BATT_Y, bz), ORANGE)
# Positive/negative cap rings
for i, (bx, bz) in enumerate(cell_pos):
    make_cylinder(f"BattCap_{i}",  CELL_R + 2, 4, (bx, BATT_Y + CELL_H, bz), SILVER)
# Holder tray
make_box("BatteryTray", 115, 10, 70, (-63, BATT_Y - 10, -35), SILVER)

BATT_TOP = BATT_Y + CELL_H

# ==========================================================================
# ELECTRONICS STACK   Y = BATT_TOP + 30 … ~1050
# ==========================================================================

EL_Y = BATT_TOP + 35

# IDU — thin rectangular slab
make_box("IDU", 145, 14, 95, (-72, EL_Y, -47), CYAN)
# IDU connector strip
for ci in range(8):
    make_box(f"IDU_Pin_{ci}", 4, 8, 4, (-60 + ci * 15, EL_Y + 14, -48), SILVER)
EL_Y += 28

# Internal Sensor Pack — slab with bump sensors
make_box("InternalSensorPack", 135, 22, 85, (-67, EL_Y, -42), CYAN)
for si in range(5):
    make_cylinder(f"SensorDome_{si}", 6, 12, (-52 + si * 24, EL_Y + 22, 0), YELLOW)
EL_Y += 38

# KDU
make_box("KDU_Body",      85, 28, 55, (-42, EL_Y, -27), CYAN)
make_box("KDU_Connector", 14, 14, 12, ( 43, EL_Y + 7,  -7), SILVER)
make_box("KDU_LED",        5,  5,  5, (-40, EL_Y + 28, -5), (0.0, 1.0, 0.0))
EL_Y += 46

# Faraday Cage — hollow shell + inner converter module
CAGE_W, CAGE_H, CAGE_D = 170, 75, 120
hollow_shell("FaradayCage", CAGE_W, CAGE_H, CAGE_D, 6,
             (-CAGE_W / 2, EL_Y, -CAGE_D / 2), DKGRAY, transparency=30)
# Faraday cage top lid (separate so it looks removable)
make_box("FaradayCage_Lid", CAGE_W, 6, CAGE_D,
         (-CAGE_W / 2, EL_Y + CAGE_H, -CAGE_D / 2), DKGRAY)
# Fiber-optic Ethernet Converter inside
make_box("FiberOpticConverter", 85, 38, 65, (-40, EL_Y + 18, -30), YELLOW)
# SFP / fiber port stubs on the front face
for fp in range(4):
    make_cylinder(f"FiberPort_{fp}", 3, 18,
                  (44, EL_Y + 22 + fp * 8, -5), GREEN)
# Ethernet RJ45 ports on the back
for ep in range(2):
    make_box(f"RJ45_Cage_{ep}", 16, 14, 8,
             (-42, EL_Y + 28, 58 - ep * 20), SILVER)
EL_Y += CAGE_H + 20

# Teensy boards x3 — micro-controller PCBs
for ti in range(3):
    make_box(f"Teensy_{ti:03d}", 58, 5, 20, (-29, EL_Y + ti * 15, -10), YELLOW)
    # USB micro connector
    make_box(f"Teensy_USB_{ti}", 8, 5, 4, (29, EL_Y + ti * 15 + 1, -2), SILVER)
    # Reset button
    make_cylinder(f"Teensy_Btn_{ti}", 2, 3,  (-24, EL_Y + ti * 15 + 5,  8), RED)
TEENSY_TOP = EL_Y + 3 * 15 + 5
EL_Y = TEENSY_TOP + 18

# Taidecent module — compact RF module
make_box("Taidecent_Body",    75, 14, 45, (-37, EL_Y, -22), YELLOW)
make_cylinder("Taidecent_Ant", 3, 55, (-30, EL_Y + 14, -10), SILVER)
EL_Y += 28

# Intel Compute Stick — long thin form factor
make_box("IntelComputeStick", 105, 20, 28, (-52, EL_Y, -14), SILVER)
make_box("ComputeStick_USB_A", 15, 12, 10, ( 53, EL_Y + 4, -5), DKGRAY)
make_box("ComputeStick_HDMI",  12, 8,  5,  (-57, EL_Y + 6, -4), DKGRAY)
EL_Y += 36

# Ethernet Shields x2 — full Arduino-shield sized PCBs
for ei in range(2):
    make_box(f"EthernetShield_{ei:03d}", 135, 7, 85,
             (-67, EL_Y + ei * 18, -42), GREEN)
    make_box(f"EthShield_RJ45_{ei}", 18, 15, 15,
             (67, EL_Y + ei * 18, -7), SILVER)
    # Header pins row
    for pi in range(14):
        make_cylinder(f"EthPin_{ei}_{pi}", 1, 10,
                      (-60 + pi * 9, EL_Y + ei * 18 + 7, -40), SILVER)

ELEC_TOP = EL_Y + 2 * 18 + 7

# ==========================================================================
# TOP SHELL — exploded cube assembly
# ==========================================================================

SHELL_Y1 = ELEC_TOP + 60
SS = 290   # shell inner size
WALL1, WALL2, WALL3 = 20, 22, 15

# Innermost: Ballistic Steel Lining
hollow_shell("BallisticSteelLining",
             SS, SS, SS, WALL1,
             (-SS / 2, SHELL_Y1, -SS / 2), CYAN, transparency=20)

# Middle: Concrete shell (exploded 80 mm above)
SHELL_Y2 = SHELL_Y1 + SS + 80
MID_S = SS + 2 * WALL1 + 20
hollow_shell("ConcreteShell",
             MID_S, MID_S, MID_S, WALL2,
             (-MID_S / 2, SHELL_Y2, -MID_S / 2), GREEN, transparency=20)

# Outer: ABS illuminated skin (exploded 80 mm above concrete)
SHELL_Y3 = SHELL_Y2 + MID_S + 80
ABS_S = MID_S + 2 * WALL2 + 20
hollow_shell("ABSSkin",
             ABS_S, ABS_S, ABS_S, WALL3,
             (-ABS_S / 2, SHELL_Y3, -ABS_S / 2), MAGENTA, transparency=15)

# ABS corner bracket cubes (interlock detail, 8 corners)
for cx in [-1, 1]:
    for cz in [-1, 1]:
        bx = cx * ABS_S / 2 - cx * 25
        bz = cz * ABS_S / 2 - cz * 25
        make_box(f"ABSCorner_{cx}_{cz}", 35, 35, 35,
                 (bx - 17, SHELL_Y3 + ABS_S - 35, bz - 17), MAGENTA)

# LED strips embedded in ABS skin (thin coloured strips on each face top edge)
for face, (lx, ly, lz, lw, lh, ld) in enumerate([
    (-ABS_S/2,       SHELL_Y3 + ABS_S - 6, -ABS_S/2,  ABS_S, 6, 8),   # front top
    (-ABS_S/2,       SHELL_Y3 + ABS_S - 6,  ABS_S/2 - 8, ABS_S, 6, 8), # back top
]):
    make_box(f"ABSLEDStrip_{face}", lw, lh, ld, (lx, ly, lz), (0.9, 0.9, 1.0))

# ==========================================================================
# CONNECTIVITY CLUSTER  (offset to +X side)
# ==========================================================================

CX   = 430
CY0  = BASE_TOP + 20   # align with lower mid-section

# Console / CRT monitor
CON_W, CON_H, CON_D = 210, 170, 35
make_box("Console_Housing",  CON_W, CON_H, CON_D,
         (CX, CY0, -CON_D / 2), RED)
make_box("Console_Bezel",    CON_W - 20, CON_H - 20, 8,
         (CX + 10, CY0 + 10, -CON_D / 2 - 8), DKGRAY)
make_box("Console_Screen",   CON_W - 40, CON_H - 40, 4,
         (CX + 20, CY0 + 20, -CON_D / 2 - 12), (0.05, 0.05, 0.1))
make_box("Console_Stand",    22, 70, 28,
         (CX + 94, CY0 - 70, -14), SILVER)
make_box("Console_FootBase", 130, 12, 70,
         (CX + 40, CY0 - 82, -35), SILVER)
# Keyboard suggestion
make_box("Console_Keyboard", 160, 8, 60,
         (CX + 25, CY0 - 90, -30), DKGRAY)

# Data Cable terminator
DCAB_Y = CY0 + CON_H + 50
make_box("DataCable_Term", 45, 22, 22, (CX + 80, DCAB_Y, -11), RED)
make_cylinder("DataCable_Plug", 5, 20, (CX + 125, DCAB_Y + 7, 0), SILVER)

# Cellular data connection module
CELL_Y = DCAB_Y + 55
make_box("CellularModule",   65, 22, 32, (CX + 70, CELL_Y, -16), RED)
make_cylinder("CellAnt_1",   3, 45, (CX + 135, CELL_Y + 22, -5), SILVER)
make_cylinder("CellAnt_2",   3, 45, (CX + 145, CELL_Y + 22,  5), SILVER)

# LoRa module
LORA_Y = CELL_Y + 60
make_box("LoRa_Module",     55, 30, 22, (CX + 70, LORA_Y, -11), RED)
make_cylinder("LoRa_Ant",    3, 80, (CX + 125, LORA_Y + 30,  0), SILVER)
make_box("LoRa_SMAConn",    10, 10, 6,  (CX + 125, LORA_Y + 20, -3), DKGRAY)

# Starlink dish
STAR_Y = LORA_Y + 120
DISH_R = 130
# Primary dish (wide shallow cone)
make_cone("StarlinkDish_Primary", DISH_R, 8, 50,
          (CX + DISH_R / 2 - 30, STAR_Y, -DISH_R / 2 + 30), RED)
# Sub-reflector (small cone at feed point)
make_cone("StarlinkDish_SubRef",  28, 4, 18,
          (CX + DISH_R / 2 + 20, STAR_Y + 45, 0), RED)
# Feed arm
make_cylinder("StarlinkFeedArm", 5, 60,
              (CX + DISH_R / 2 + 5, STAR_Y, 0), SILVER)
# Mast
make_cylinder("StarlinkMast", 9, 130,
              (CX + DISH_R / 2 - 30 + DISH_R / 2, STAR_Y - 130, 0), SILVER)
# Base plate
make_box("StarlinkMountBase", 90, 18, 90,
         (CX + DISH_R / 2 - 30 + DISH_R / 2 - 45, STAR_Y - 148, -45), SILVER)

# Approximate cable from Starlink back to Faraday cage area
# (represented as a narrow cylinder running vertically)
CABLE_X = CX + 20
make_cylinder("Cable_StarToMain", 5, STAR_Y - (ELEC_TOP - 20),
              (CABLE_X, ELEC_TOP - 20, 0), DKGRAY)

# ==========================================================================
# Final document recompute and view
# ==========================================================================

doc.recompute()

try:
    import FreeCADGui as Gui
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
    print("View set to Isometric and fitted.")
except Exception:
    pass

obj_count = len(doc.Objects)
print("=" * 60)
print("  Blueprint Assembly — generation complete!")
print(f"  Objects created : {obj_count}")
print("=" * 60)
print()
print("Rendering tips:")
print("  • View > Draw Style > Shaded  for solid rendering")
print("  • View > Draw Style > Wireframe  to inspect shell layers")
print("  • Select a component in the Model tree and press Space")
print("    to toggle its visibility.")
print("  • File > Export > STL / STEP / OBJ for external renderers")
print("    (Blender, KeyShot, etc.)")
print()
print("Layer colour guide:")
print("  Magenta  = ABS skin / load cells / legs")
print("  Green    = Concrete layers / Ethernet shields")
print("  Cyan     = Ballistic steel / electronics")
print("  Red      = Connectivity cluster")
print("  Orange   = Power components")
print("  Yellow   = PCB modules")
print("  Silver   = Metal hardware / connectors")
print("  DkGray   = Faraday cage / screen bezels")