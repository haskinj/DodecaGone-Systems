# Tools — DodecaGone Systems

**Last updated:** February 2026  
**Maintainer:** Jesse Haskin  
**Status:** Reference documentation (proprietary)

---

## Overview

This directory contains utility scripts, experimental software, and demonstration projects developed within DodecaGone Systems. Tools are categorized by function and language. Source code is maintained in this repository for reference and internal use.

---

## Research Tools

### NeuroSync

**Language:** Python  
**Lines:** 639  
**Description:** Telemetry tool for cross‑referencing FlowTime EEG biometric data with Sanding Scale cognitive load reports. Provides a tkinter interface for loading CSV exports, aligning with conversation logs, and generating synchronized visualizations. Supports manual data entry for sessions without biometric capture.

**Key features:**
- Imports FlowTime CSV (gamma, beta, alpha, theta, delta, heart rate, HRV)
- Loads conversation logs in text or JSON format
- Timeline view with clickable session navigation
- Brainwave distribution bars and vitals panel
- JSON export for persistence

---

### Sanding Scale Tracker

**Language:** HTML/JavaScript  
**Description:** Browser‑based tool for real‑time cognitive load monitoring. Allows input of current sanding level (0.0–12.0+), displays behavioral anchors at each threshold, and tracks session history. Designed for use during AI interactions to provide immediate context to agents.

**Key features:**
- Interactive slider or numeric input
- Color‑coded threshold indicators (green, yellow, red, black)
- Session log with timestamps
- Export to JSON for integration with other tools

---

### MTGPython

**Language:** Python  
**Description:** Educational tool that teaches Python through Magic: The Gathering card mechanics. Translates card text into Python classes, demonstrating object‑oriented programming, conditionals, and state management using a domain familiar to many developers.

**Key features:**
- Card class hierarchy (creatures, instants, sorceries, enchantments)
- Combat phase simulation
- Stack and priority mechanics
- Tutorial mode with progressive complexity

---

## Experimental Languages

### FrogPond

**Language:** Custom (interpreter in Python)  
**Description:** A haiku‑based programming language. Programs must be written in valid 5‑7‑5 syllable structure. The interpreter validates syllable count, parses keywords, and executes the resulting logic. Includes a REPL for interactive exploration.

**Key features:**
- Syllable counter (dictionary‑based with fallback)
- Keyword set optimized for haiku construction
- Error messages that respect the poetic form
- Example programs demonstrating loops, conditionals, and I/O

---

### PleaseScript

**Language:** Python (interpreter)  
**Description:** A language with no whitespace and mandatory manners. All whitespace is stripped during lexing. Commands execute only if they begin with the word `please`. Rude instructions are silently ignored. Blocks are delimited by curly braces.

**Key features:**
- Whitespace‑agnostic parser
- Politeness enforcement layer
- Basic arithmetic, variables, and control flow
- Example: `please print "Hello world"` works; `print "Hello world"` does nothing

---

## Experimental Artifacts (Wonkys)

### Entropic Atomic Hostility

**Language:** HTML/CSS/JavaScript  
**Description:** Win95‑style window containing a live seismograph. Pressing "Get Value" displays nine instances of the word "help." Closing the window produces a custom Blue Screen of Death. The hostility is permanent.

**Key features:**
- Canvas‑based seismograph animation
- Retro window chrome (title bar, buttons, status bar)
- Progressive despair mechanics

---

### Win95 Melting Folders

**Language:** HTML/CSS/JavaScript  
**Description:** A "My Computer" window where folder icons progressively melt when double‑clicked. After all folders have melted, a message appears: "All melted away...". Reload to reset.

**Key features:**
- CSS keyframe melt animation
- Emoji‑based folder icons
- Status bar reads: "Just try your best I guess?"

---

### SOUL_RADIO

**Language:** HTML/JavaScript (Web Audio API)  
**Version:** 1.1  
**Description:** Audio synthesizer with retro interface. Generates sound from configurable waveforms (sine, square, sawtooth, triangle). Includes frequency and gain controls.

**Key features:**
- Real‑time waveform generation
- Oscillator selection and mixing
- Visual VU meter
- Preset storage

---

### ASCII_CHAOS

**Language:** COBOL  
**Description:** Experimental text artifact written in COBOL. Generates random ASCII patterns in a terminal. Demonstrates the use of a 1959‑vintage language for modern absurdist purposes.

**Key features:**
- Compiled with GnuCOBOL
- Random character generation
- Configurable screen dimensions
- Includes `README.txt` explaining the absurdity

---

### progresspanic.py

**Language:** Python  
**Description:** A loading bar that panics. Progress climbs slowly. At 85%, a group of "oh no" labels appears. At 90%, a larger "OH NO" appears. At 95%, it flashes "OH NO!!". At 99%, the program exits and creates a `README.txt` file filled with variations of "oh no" and "why why why".

**Key features:**
- Tkinter GUI with Windows 3.1 aesthetic
- Escalating panic stages
- Haunted README generation

---

### PyDeck Cards

**Language:** HTML/CSS/JavaScript  
**Description:** Collectible card game template system for learning Python. Cards represent programming concepts with rarity, cost, and combat stats. Bug encounter cards serve as enemies.

**Key features:**
- Card design with CSS
- Deck builder interface
- Battle simulator (JavaScript)
- Python code generation from card combinations

---

## Proprietary Notice

All tools, scripts, and associated documentation are the intellectual property of DodecaGone Systems. This material is provided for reference purposes only and may not be reproduced, distributed, or used without explicit written permission.

---

*DodecaGone Systems — Distributed AI Coordination Research*
