// compute ram from 1 + 2 + ... + RAM[0]

// n = RAM[0]
// i = 1
// sum = 0

// LOOP:
//      if i > n goto STOP
//      sum = sum + i
//      i = i + 1
//      goto LOOP
// STOP:
//      R1 = sum


// first part: variable initialization:

        @R0
        D=M

        @N
        M=D             // N = RAM[0]

        @I
        M=1             // I = 1

        @SUM
        M=0             // SUM = 0

// second part: loop:

(LOOP)
        @I
        D=M

        @N
        D=D-M           // I - N

        @STOP
        D;JGT           // If I-N > 0 (basically i > n), stop


        @SUM
        D=M

        @I
        D=D+M           // SUM + I

        @SUM
        M=D             // SUM = SUM + I 

        @I
        M=M+1           // I = I + 1

        @LOOP
        0;JMP

(STOP)
        @SUM
        D=M

        @R1
        M=D             // RAM[1] = SUM

(END)
        @END
        0;JMP
