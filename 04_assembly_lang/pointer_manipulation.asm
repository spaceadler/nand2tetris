// for (i=0; i<n; i++)
// {
//        arr[i] =- 1
// }

// Suppose that arr=100 and n=10


// variable declataion: i = 0, n = 10, arr = 100.

        @I
        M=0             // I = 0

        @N
        M=10            // N = 10

        @ARR
        M=100           // ARR = 100

// make a loop that does the following:
//
// loop: if i == n then end, else continue
//
// RAM[arr+i] to be set to -1
// i = i + 1
//
// return to loop
//
// end

(LOOP)
        @N
        D=M

        @I
        D=D-M   // n - i

        @END
        0;JEQ   // If n - i = 0 (basically n = i) then jump to end, else continue

        @ARR
        D=M

        @I
        A=D+M   // arr + i
        M=-1    // take memory of arr + i (basically ram[arr + i]) and set it to -1

        @I
        M=M+1   // increment i

        @LOOP
        0;JMP   // loop again
(END)
        @END
        0;JMP   // end
