# NAND2Tetris: A 16-bit Computer from One Gate

> The Hack computer built from a single NAND gate up to a working CPU, plus its machine language.

![Architecture](https://img.shields.io/badge/Architecture-16--bit%20Von%20Neumann-blue)
![Hardware](https://img.shields.io/badge/Hardware-HDL-orange)
![Status](https://img.shields.io/badge/Part%201-Complete-success)

## Overview

Every chip here derives from `Nand` (plus the course's built-in `DFF`). The point is to have no black boxes left under the kernel and embedded work that comes next.

## The Silicon Stack

```mermaid
flowchart BT
    subgraph P1["Project 1: Boolean Logic"]
        Nand --> Not & And & Or
        And & Or & Not --> Xor & Mux & DMux
        Mux --> Mux16 --> Mux4Way16 --> Mux8Way16
        DMux --> DMux4Way --> DMux8Way
    end
    subgraph P2["Project 2: Arithmetic"]
        HalfAdder --> FullAdder --> Add16 --> Inc16
        Add16 --> ALU
    end
    subgraph P3["Project 3: Memory"]
        DFF --> Bit --> Register --> RAM8 --> RAM64 --> RAM512 --> RAM4K --> RAM16K
        Register --> PC
    end
    subgraph P5["Project 5: Computer"]
        CPU --> Computer
        Memory --> Computer
    end
    Xor --> HalfAdder
    Mux16 --> ALU
    Inc16 --> PC
    ALU --> CPU
    PC --> CPU
    RAM16K --> Memory
```

## The Hardware, Wire by Wire

Every diagram below is drawn from its `.hdl` file: boxes are parts, edge labels are the actual wire names.

### Memory (`05_Computer/Memory.hdl`)

```mermaid
flowchart LR
    load(["load"]) --> d1["DMux<br/>sel = address[14]"]
    d1 -->|ram| ram
    d1 -->|scrkey| d2["DMux<br/>sel = address[13]"]
    d2 -->|scr| scr
    d2 -.->|"key (unused: the keyboard is read-only)"| kbd

    inp(["in[16]"]) --> ram & scr
    ram["RAM16K<br/>address[0..13]"] -->|ramOut| m3
    scr["Screen<br/>address[0..12]"] -->|scrOut| m2
    kbd["Keyboard"] -->|keyOut| mk

    lo["Or8Way<br/>address[0..7]"] -->|lowBits| past["Or"]
    hi["Or8Way<br/>address[8..12]"] -->|highBits| past
    past -->|pastKbd| mk["Mux16<br/>b = false"]
    mk -->|kbdOrZero| m2["Mux16<br/>sel = address[13]"]
    m2 -->|scrKeyOut| m3["Mux16<br/>sel = address[14]"]
    m3 --> out(["out[16]"])
```

| Address | Goes to |
|---|---|
| `0x0000–0x3FFF` | RAM16K (`address[14] = 0`) |
| `0x4000–0x5FFF` | Screen (`address[14..13] = 10`) |
| `0x6000` | Keyboard (`address[14..13] = 11`, low 13 bits all 0) |
| above `0x6000` | reads 0 (`pastKbd` zeroes the keyboard path) |

### ALU (`02_Boolean_Arithmetic/ALU.hdl`)

```mermaid
flowchart LR
    x(["x[16]"]) --> zx["Mux16<br/>sel = zx, b = 0"]
    zx -->|xmux| nx["Mux16<br/>sel = nx"]
    zx -->|xmux| notx["Not16"] -->|notxmux| nx
    y(["y[16]"]) --> zy["Mux16<br/>sel = zy, b = 0"]
    zy -->|ymux| ny["Mux16<br/>sel = ny"]
    zy -->|ymux| noty["Not16"] -->|notymux| ny

    nx -->|xmux2| and16["And16"] & add16["Add16"]
    ny -->|ymux2| and16 & add16
    and16 -->|xyand| f["Mux16<br/>sel = f"]
    add16 -->|xyadd| f
    f -->|outmux| no["Mux16<br/>sel = no"]
    f -->|outmux| noto["Not16"] -->|notoutmux| no
    no --> out(["out[16]"])

    no -->|"out[15]"| ng(["ng"])
    no -->|"zr1 = out[0..7]"| o1["Or8Way"]
    no -->|"zr2 = out[8..15]"| o2["Or8Way"]
    o1 -->|or1| or["Or"]
    o2 -->|or2| or
    or -->|nonzero| not["Not"] --> zr(["zr"])
```

Six control bits pick 18 functions: `zx nx` prepare `x`, `zy ny` prepare `y`, `f` chooses add or and, and `no` negates the result.

### CPU (`05_Computer/CPU.hdl`): where the ALU lives

```mermaid
flowchart LR
    ins(["instruction[16]"]) --> amux["Mux16<br/>sel = instruction[15]"]
    amux -->|aMuxOut| areg["ARegister<br/>load = aRegLoad"]
    areg -->|aRegOut| ymux["Mux16<br/>sel = instruction[12]"]
    inM(["inM[16]"]) --> ymux
    ymux -->|aOrM| alu
    dreg["DRegister<br/>load = loadD"] -->|outD| alu["ALU<br/>zx..no = instruction[11..6]"]
    alu -->|aluOut| amux & dreg
    alu -->|outM| outM(["outM[16]"])
    areg -->|"addressM = aRegOut[0..14]"| addr(["addressM[15]"])

    alu -->|"zr, ng"| jmp["jump logic<br/>jlt · jeq · jgt from instruction[2..0]"]
    jmp -->|"PCload (gated by instruction[15])"| pc["PC<br/>inc = true"]
    areg -->|aRegOut| pc
    rst(["reset"]) --> pc
    pc -->|"pc[0..14]"| pcout(["pc[15]"])
    ins -->|"instruction[15] and [3]"| wm(["writeM"])
```

| Control wire | Built from | Means |
|---|---|---|
| `aRegLoad` | `not i[15]` or (`i[15]` and `i[5]`) | A-instruction, or a C-instruction with `d1` |
| `loadD` | `i[15]` and `i[4]` | C-instruction with `d2` |
| `writeM` | `i[15]` and `i[3]` | C-instruction with `d3` |
| `PCload` | `i[15]` and (`jlt` or `jeq` or `jgt`) | the jump condition holds; `pos = not (zr or ng)` |

### The Computer (`05_Computer/Computer.hdl`): how they connect

```mermaid
flowchart LR
    rom["ROM32K<br/>the program"] -->|application| cpu["CPU"]
    cpu -->|counter| rom
    cpu -->|"memin (outM)"| mem["Memory"]
    cpu -->|"memload (writeM)"| mem
    cpu -->|"memaddress (addressM)"| mem
    mem -->|"memOut (inM)"| cpu
    reset(["reset"]) --> cpu
```

One cycle: `ROM32K[counter]` is the instruction, the CPU computes it against `memOut`, writes `memin` to `memaddress` when `memload` is set, and the PC picks the next `counter`.

## Software

```mermaid
flowchart LR
    asm[".asm"] -->|"assembler.py (2 passes)"| hack[".hack"] --> ROM32K
```

| File | What it does |
|---|---|
| `flip.asm` | Swaps `RAM[0]` and `RAM[1]` |
| `sum_1_to_n.asm` | `RAM[1] = 1 + 2 + … + RAM[0]` |
| `pointer_manipulation.asm` | `arr[i] = -1` for `i < 10`, `arr = 100` |
| `assembler/assembler.py` | Hack assembler: labels, variables from `RAM[16]`, every `comp`/`dest`/`jump` |

> **About the assembler:** the original was written for Project 6 and then lost (only an empty file survived). The current `assembler.py` is a **stand-in replacement written by an AI assistant**, so the toolchain works end to end. It is not the original work.

```bash
python 04_Assembly_Lang/assembler/assembler.py 04_Assembly_Lang/sum_1_to_n.asm   # → sum_1_to_n.hack
```

## Simulation

Load any `.hdl` into the [Nand2Tetris Web IDE](https://nand2tetris.github.io/web-ide/chip/) with its course `.tst` script.

## Progress

- [x] **Project 1:** Boolean Logic
- [x] **Project 2:** Boolean Arithmetic
- [x] **Project 3:** Sequential Logic
- [x] **Project 4:** Machine Language
- [x] **Project 5:** Computer Architecture (CPU, Memory, Computer). *Part 1 hardware complete.*
- [x] **Project 6:** The Assembler *(original lost; AI-written replacement in place)*
- [ ] **Projects 7–8:** VM Translator
- [ ] **Project 9:** High-Level Language (Jack)
- [ ] **Projects 10–11:** Compiler
- [ ] **Project 12:** Operating System

---
*powered by logic, coffee, and many sleepless nights*
