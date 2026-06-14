// Program: flip.asm
// flips the values of
// RAM[0] and RAM[1]

// temp = R1
// R1 = R0
// R0 = temp

        @R1
        D=M

        @TEMP
        M=D // TEMP = R1

        @R0
        D=M

        @R1
        M=D // R1 = R0

        @TEMP
        D=M

        @R0
        M=D // R0 = TEMP

(END)
        @END
        0;JMP
