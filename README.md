# NAND2Tetris: A 16-bit General Purpose Computer

> A "First Principles" implementation of a full-scale 16-bit computer architecture, built from the NAND gate up to the Operating System.
> 
![Architecture](https://img.shields.io/badge/Architecture-16--bit%20Von%20Neumann-blue)
![Hardware](https://img.shields.io/badge/Hardware-HDL-orange)
![Software](https://img.shields.io/badge/Software-Jack%20(Java--like)-success)

### Table of Contents

* [Overview](#overview)
* [The Silicon Substrate](#the-silicon-substrate)
* [Architecture](#architecture)
* [The ALU](#the-alu)
* [Memory Hierarchy](#memory-hierarchy)


* [The Software Stack](#the-software-stack)
* [Machine Language](#machine-language)
* [The Compiler](#the-compiler)


* [Simulation](#simulation)
* [Progress Log](#progress-log)

# Overview

If you want to use a computer, you can buy a MacBook. If you want to understand computer science, you can read a textbook.

But if you want to know what a machine is really made of, you have to build one.

Modern computing is obscured by layers of abstraction. We take the CPU, the kernel, and the compiler for granted. This project is a rejection of that "black box" mentality.

The "Hack Computer" is a general-purpose 16-bit computer constructed entirely from scratch. Every chip in this repository is derived from a single logic gate: the NAND, in a "First Principles" fashion. The goal is to lay the groundwork for future kernel and embedded systems development (specifically Ring-0 development) by demystifying the stack completely.

# The Silicon Substrate

The following dependency graph illustrates the genesis of the system: from the Nand to where I currently am (both the ALU and the Memory Units).

```mermaid
graph TD
    %% 1. BOOLEAN LOGIC
    subgraph Logic ["Phase 1: Boolean Logic"]
        Nand["Nand"]
        And["And"]
        Or["Or"]
        Mux["Mux"]
        DMux["DMux"]
        
        Nand --> And
        Nand --> Or
        Nand --> Mux
        Nand --> DMux
    end

    %% 2. BOOLEAN ARITHMETIC
    subgraph Arithmetic ["Phase 2: Boolean Arithmetic"]
        HA[HalfAdder]
        FA[FullAdder]
        ALU[ALU]
    end

    %% 3. SEQUENTIAL LOGIC
    subgraph Sequential ["Phase 3: Sequential Logic"]
        DFF["DFF (Time Primitive)"]
        Bit["Bit"]
        Register["Register (16-Bit)"]
        RAM4K
        RAM16K
    end

    %% --- WIRING & DETAILS ---

    %% HALF ADDER DETAIL (Sum = Xor, Carry = And)
    And -->|"Carry Bit"| HA
    Or -->|"Sum Logic (Xor)"| HA
    Nand -->|"Sum Logic (Xor)"| HA

    %% FULL ADDER (Built from HA + Or)
    HA --> FA
    Or -->|"Carry Propagation"| FA

    %% ALU DETAIL (The Calculation Engine)
    FA -->|"Addition (f=1)"| ALU
    And -->|"Bitwise And (f=0)"| ALU
    Mux -->|"Control Logic (zx, nx, zy, ny, f, no)"| ALU
    Or -->|"Output Flags (zr, ng)"| ALU

    %% SEQUENTIAL / MEMORY RECURSION
    DFF -->|"Feedback Loop"| Bit
    Mux -->|"Load/Keep Selection"| Bit
    
    Bit -->|x16| Register
    
    %% The Abstracted Recursion
    Register -.->|"Recursive Layering (x8...)"| RAM4K
    RAM4K -.->|x4| RAM16K

```

# Architecture

The system utilizes the classic 16-bit Von Neumann architecture, integrating the CPU, RAM, and ROM via a centralized bus system. The hardware is implemented in Hardware Description Language (HDL).

## The ALU

The compute engine. It utilizes a series of `Mux16` and `Add16` gates to perform 18 different computations based on just 6 control bits:

1. zx: Zero the x input
2. nx: Negate (Not) the x input
3. zy: Zero the y input
4. ny: Negate (Not) the y input
5. f: Function code (1 for Add, 0 for And)
6. no: Negate (Not) the output

It also outputs status flags (`zr` for zero, `ng` for negative) to support branching logic in the CPU.

<img width="1621" height="332" alt="Screenshot 2026-01-19 120720" src="https://github.com/user-attachments/assets/f58496d1-ceef-44d2-9326-34bbd03097f8" />

## The Memory

The RAM16K is a recursive hierarchy design. I constructed this by chaining `RAM4K` modules, which themselves are built from `RAM512`, down to the single Bit Register. This ensures efficient address access via `DMux` logic.

<img width="792" height="445" alt="Screenshot 2026-01-19 121538" src="https://github.com/user-attachments/assets/22645755-f679-435b-8464-4735220d7a9f" />

# The Software Stack

Hardware is useless without instructions. The second half of this project focuses on virtualization and compilation.

### Machine Language

The Hack platform uses a 16-bit A-instruction and C-instruction set. Below is an example of a simple loop (Sum 1 to 10) in Hack Assembly:

```asm
// Computes R0 = 1 + ... + 10
   @i     // Allocates memory for i
   M=1    // i = 1
   @sum   // Allocates memory for sum
   M=0    // sum = 0

(LOOP)
   @i
   D=M    // D = i
   @10
   D=D-A  // D = i - 10
   @END
   D;JGT  // If (i - 10) > 0, goto END

   @i
   D=M
   @sum
   M=D+M  // sum = sum + i
   @i
   M=M+1  // i = i + 1
   @LOOP
   0;JMP  // Goto LOOP

(END)
   @END
   0;JMP  // Infinite loop

```

### The Compiler

The final goal is to run a high-level Object-Oriented language called Jack. The compiler stack includes:

1. Assembler: Translates `.asm` to binary `.hack`.
2. VM Translator: Converts stack-based VM code to Assembly.
3. Jack Compiler: Tokenizes and parses high-level Java-like syntax into VM code.

# Simulation

Every chipset made here has passed all hardware simulation tests in the course-provided Hardware Simulator.

To run the HDL simulations:

1. Clone the repo.
2. Load the `.hdl` files into the [Nand2Tetris Web IDE](https://nand2tetris.github.io/web-ide/chip/).
3. Load the corresponding test script `.tst`.
4. Run the simulation.

# Progress Log

### I. Hardware Layer (The Silicon)

* [x] **Project 1:** Boolean Logic (Nand, And, Or, Mux, DMux)
* [x] **Project 2:** Boolean Arithmetic (HalfAdder, FullAdder, ALU)
* [x] **Project 3:** Sequential Logic (DFF, Bit, Register, RAM8/64/4K/16K)
* [ ] **Project 4:** Machine Language <--- Currently here
* [ ] **Project 5:** Computer Architecture (CPU & Memory Mapping)

### II. Software Hierarchy (The Virtualization)

* [ ] **Project 6:** The Assembler
* [ ] **Project 7/8:** VM Translator (Stack Arithmetic & Control Flow)
* [ ] **Project 9:** High-Level Language (Jack) Application
* [ ] **Project 10/11:** The Compiler (Syntax Analysis & Code Gen)
* [ ] **Project 12:** The Operating System (Math.jack, Screen.jack, etc.)

---

*powered by logic, coffee, and many sleepless nights*
