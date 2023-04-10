# **Hack Assembler 💻📟**
![Hack Assembler Banner](assets/Hack_Assembler_Banner.png)

## **Description**
🟡 ***Assembler*** is a tool used to convert a Hack Assembly Language program, which is a text file with a .asm extension, into binary machine code (Hack Machine Language). The resulting machine code is then saved to a new file with a .hack extension. <br>
🟠 The process of assembly is carried out in multiple phases. First, it starts by checking for labels and variables and updates it inside their corresponding dictionary. Then, the variables and labels are substituted with corresponding values and storing the changed values inside a new file called "**New.asm**". <br>
🔴 Then, the modified file **"New.asm"** is passed for proper conversion. Each line is read as string and converting them to their respective binary equivalents into a file named 
*(Original_file_name).hack* . All the Implementation are done in Python. <br>

#### **Types of Instruction**
* **A-Instruction** : Addressing Instruction
* **C-Instruction** : Computation Instruction


## **Example**
#### **Max.asm**
```
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/max/Max.asm

// Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])

   @R0
   D=M              // D = first number
   @R1
   D=D-M            // D = first number - second number
   @OUTPUT_FIRST
   D;JGT            // if D>0 (first is greater) goto output_first
   @R1
   D=M              // D = second number
   @OUTPUT_D
   0;JMP            // goto output_d
(OUTPUT_FIRST)
   @R0             
   D=M              // D = first number
(OUTPUT_D)
   @R2
   M=D              // M[2] = D (greatest number)
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP            // infinite loop

```

#### **Max.hack**
```
0000000000000000
1111110000010000
0000000000000001
1111010011010000
0000000000001010
1110001100000001
0000000000000001
1111110000010000
0000000000001100
1110101010000111
0000000000000000
1111110000010000
0000000000000010
1110001100001000
0000000000001110
1110101010000111
```