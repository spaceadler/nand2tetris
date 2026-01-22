# 16-Bit Hack Platform: From NAND to OS
> A "First Principles" implementation of a full-scale computer architecture.

## Desired System Architecture:
* Architecture: [16-bit Von Neumann](https://en.wikipedia.org/wiki/Von_Neumann_architecture)
* Hardware: HDL Implementation of a CPU, RAM, and ALU (as well as all the required logic gates)
* Software: Assembler, Virtual Machine Translator, and Compiler completely self-written.
* OS: Standard Library (Math, Screen, Keyboard, and String) written in a Java-like language called Jack.

## Motivation

Computers are a black box. Some use them to surf the web, process words, and send emails. While others take the high levels of abstraction for granted and build things. But in order to achieve a deeper understanding of the Computer Sciences subject, I want to know what they are *really* made of. For this reason, I need to build up the abstractions myself and use them, to eventually transfer this knowledge to other domains. This is why I'm currently building a general purpose 16-bit computer called the (Hack Computer), starting from the NAND gate, and ending with a high level OS running Tetris with a goal of laying the groundwork for future kernel and embedded systems development (specific interest in Ring-0 development).

## Implementation
Every chipset made here is derived from NAND in a "First Principles" fashion, where the NAND would contribute to the AND, MUX, their 16-bit versions, ADDER's, ALU's, RAM components, and eventually the Machine Language and CPU.

Every chipset has passed all hardware simulation tests, in the course-provided Hardware Simulator. [here](https://nand2tetris.github.io/web-ide/chip/).

## General Overview
The Silicon Substrate: From Logic Gates to Memory Arrays:

 ```mermaid
graph TD
    %% 1. BOOLEAN LOGIC (The Alphabet)
    subgraph Logic ["Phase 1: Boolean Logic"]
        Nand["Nand (The God Particle)"]
        
        Nand --> And
        Nand --> Or
        Nand --> Mux
        Nand --> DMux
    end

    %% 2. BOOLEAN ARITHMETIC (The Math)
    subgraph Arithmetic ["Phase 2: Boolean Arithmetic"]
        HA[HalfAdder]
        FA[FullAdder]
        ALU[ALU]
    end

    %% 3. SEQUENTIAL LOGIC (The State)
    subgraph Sequential ["Phase 3: Sequential Logic"]
        DFF["DFF (Time Primitive)"]
        Bit["Bit"]
        Register["Register (16-Bit)"]
        RAM8
        RAM64
        RAM512
        RAM4K
        RAM16K
    end

    %% CROSS-LAYER DEPENDENCIES
    
    %% Arithmetic relies on Logic
    And --> HA
    HA --> FA
    Or --> FA
    FA --> ALU
    Mux --> ALU
    And -->|Control Bits| ALU
    Or -->|Control Bits| ALU

    %% Sequential relies on Logic (Mux) and Time (DFF)
    DFF --> Bit
    Mux -->|Selection| Bit
    
    %% Recursive Memory Construction
    Bit --> Register
    Register --> RAM8
    RAM8 -->|x8| RAM64
    RAM64 -->|x8| RAM512
    RAM512 -->|x8| RAM4K
    RAM4K -->|x4| RAM16K
```

## Technical Deep Dive: The ALU and RAM diagrams
To demonstrate the architectural logic, both the ALU and RAM are the best implementations to showcase; those 2 modules form the backbone of the CPU, where Boolean and Arithmetic computations and memory management are made.

### ALU
The compute engine. It utilizes a series of Mux16 and Add16 gates to perform 18 different computations based on just 6 control bits (zeroing x, "not" x, zeroing y, "not" y, and/add function, "not" result) and outputs alongside status flags (if output is negative/zero) to support branching logic.

<img width="1621" height="332" alt="Screenshot 2026-01-19 120720" src="https://github.com/user-attachments/assets/f58496d1-ceef-44d2-9326-34bbd03097f8" />

### RAM16k
A recursive hierarchy design. I constructed this by chaining RAM4K modules, which themselves are built from RAM512, down to the single Bit Register. This ensures efficient address access via DMux logic.

<img width="792" height="445" alt="Screenshot 2026-01-19 121538" src="https://github.com/user-attachments/assets/22645755-f679-435b-8464-4735220d7a9f" />

## Progress Log

### I. Hardware Layer (The Silicon)
- [x] Project 1: Boolean Logic (Nand, And, Or, Mux, DMux)
- [x] Project 2: Boolean Arithmetic (HalfAdder, FullAdder, ALU)
- [x] Project 3: Sequential Logic (DFF, Bit, Register, RAM8/64/4K/16K) 
- [ ] Project 4: Machine Language <--- Currently here
- [ ] Project 5: Computer Architecture (CPU & Memory Mapping)

### II. Software Hierarchy (The Virtualization)
- [ ] Project 6: The Assembler
- [ ] Project 7/8: VM Translator (Stack Arithmetic & Control Flow)
- [ ] Project 9: High-Level Language (Jack) Application
- [ ] Project 10/11: The Compiler (Syntax Analysis & Code Gen)
- [ ] Project 12: The Operating System (Math.jack, Screen.jack, etc.)

---
*powered by logic, coffee, and sleepless nights*
