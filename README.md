# Opening the "blackbox": NAND2Tetris Implementation

## Computers are a blackbox: 
Some use them to surfe the web, processes words, and  sends emails.
Others take the high levels of abstraction for granted and build things.

But what are computers *really* made of? This is the goal of this repository.

I'm currently building a general purpose 16-bit computer called the (Hack Computer), starting from the NAND gate, and ending with a high level OS running Tetris.


## System Architecture:
* Architecture: [16-bit Von Neumann](https://en.wikipedia.org/wiki/Von_Neumann_architecture)
* Hardware: HDL Implementation of a CPU, RAM, and ALU (as well as all the required logic gates)
* Software: Assembler, Virtual Machine Translator, and Compiler completely self written.
* OS: Standard Library (Math, Screen, Keyboard, and String) written in a Java-like language called Jack.


## Progress Log

### I. Hardware Layer (The Silicon)
- [x] Project 1: Boolean Logic (Nand, And, Or, Mux, DMux)
- [x] Project 2: Boolean Arithmetic (HalfAdder, FullAdder, ALU)
- [ ] Project 3: Sequential Logic (DFF, Bit, Register, RAM8/64/4K) <--- Currently here
- [ ] Project 4: Machine Language
- [ ] Project 5: Computer Architecture (CPU & Memory Mapping)

### II. Software Hierarchy (The Virtualization)
- [ ] Project 6: The Assembler
- [ ] Project 7/8: VM Translator (Stack Arithmetic & Control Flow)
- [ ] Project 9: High-Level Language (Jack) Application
- [ ] Project 10/11: The Compiler (Syntax Analysis & Code Gen)
- [ ] Project 12: The Operating System (Math.jack, Screen.jack, etc.)
---

made possible with coffee and sleepless nights
