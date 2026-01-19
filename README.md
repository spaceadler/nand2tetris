# 16-Bit Hack Platform: From NAND to OS
> A "First Principles" implementation of a full-scale computer architecture.

## Motivation

Computers are a black box. Some use them to surf the web, process words, and send emails. While others take the high levels of abstraction for granted and build things. But in order to achieve a deeper understanding of the Computer Sciences subject, I want to know what they are *really* made of. For this reason, I need to build up the abstractions myself and use them, to eventually transfer this knowledge to other domains. This is why I'm currently building a general purpose 16-bit computer called the (Hack Computer), starting from the NAND gate, and ending with a high level OS running Tetris with a goal of laying the groundwork for future kernel and embedded systems development (specific interest in Ring-0 development).

## System Architecture:
* Architecture: [16-bit Von Neumann](https://en.wikipedia.org/wiki/Von_Neumann_architecture)
* Hardware: HDL Implementation of a CPU, RAM, and ALU (as well as all the required logic gates)
* Software: Assembler, Virtual Machine Translator, and Compiler completely self written.
* OS: Standard Library (Math, Screen, Keyboard, and String) written in a Java-like language called Jack.


## Progress Log

### I. Hardware Layer (The Silicon)
- [x] Project 1: Boolean Logic (Nand, And, Or, Mux, DMux)
- [x] Project 2: Boolean Arithmetic (HalfAdder, FullAdder, ALU)
- [x] Project 3: Sequential Logic (DFF, Bit, Register, RAM8/64/4K) 
- [ ] Project 4: Machine Language <--- Currently here
- [ ] Project 5: Computer Architecture (CPU & Memory Mapping)

### II. Software Hierarchy (The Virtualization)
- [ ] Project 6: The Assembler
- [ ] Project 7/8: VM Translator (Stack Arithmetic & Control Flow)
- [ ] Project 9: High-Level Language (Jack) Application
- [ ] Project 10/11: The Compiler (Syntax Analysis & Code Gen)
- [ ] Project 12: The Operating System (Math.jack, Screen.jack, etc.)

## Technical Deep Dive: The ALU Implementation
To show a working example example of this project, the ALU is the best example; it is basically the "brain" of the CPU; where both Boolean and Arithmetic computations are made.

```hdl

    // Handling the X
    Mux16(a=x , b=false , sel=zx , out=xmux );
    Not16(in=xmux , out=notxmux );
    Mux16(a=xmux , b=notxmux , sel=nx , out=xmux2 );
   
   // Handling the Y
    Mux16(a=y , b=false , sel=zy , out=ymux );
    Not16(in=ymux , out=notymux );
    Mux16(a=ymux , b=notymux , sel=ny , out=ymux2 );
    
   // Adding, and-ing
    And16(a=xmux2 , b=ymux2 , out=xyand );
    Add16(a=xmux2 , b=ymux2 , out=xyadd );
    
    // Final checks
    Mux16(a=xyand , b=xyadd , sel=f , out=outmux );
    Not16(in=outmux , out=notoutmux );
    
    // Final output, "if negative", and "if zero"
    Mux16(a=outmux , b=notoutmux , sel=no , out=out , out[15]=ng , out[0..7]=zr1 , out[8..15]=zr2);
    
    // Outputs "if zero"
    Or8Way(in=zr1, out=or1);
    Or8Way(in=zr2, out=or2);
    Or(a=or1, b=or2, out=nonzero);
    Not(in=nonzero, out=zr);
```

## Implementation
Every chipset made here is derived from NAND in a "First Principles" fashion, where the NAND would contribute to the AND, MUX, their 16-bit versions, ADDER's, ALU's, RAM components, and eventually the Machine Language and CPU.

Every chipset has passed all hardware simulation tests, in the course-provided Hardware Simulator. [here](https://nand2tetris.github.io/web-ide/chip/).

---
*powered by logic, coffee, and sleepless nights*
