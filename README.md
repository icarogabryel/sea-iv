# SEA M

SEA M - Syntax-Encoding Assembler (For MOOn) is a simple assembler for the MOOn IV ISA. It is written in Python 3 and is a command-line tool.

## MOOn IV Assembly Language

The MOOn IV assembly language is a low-level programming language that is used to write programs for the MOOn IV ISA. The MOOn IV assembly language is a human-readable representation of the machine code that is executed by the MOOn IV processor. In this language, we have instructions, pseudo-instructions, directives, labels and pointers.

### Grammar

The grammar of the MOOn IV assembly language is defined as follows:

```EBNF

asmCode = [textField] ;
textField = ".text", instList ;
instList = (inst | labelDec inst), [instList] ;
inst = rTypeInst ;
rTypeInst = MNEMONIC, AC_REG, ",", RF_REG, ",", RG_REG ;
labelDec = LABEL_ID, ':' ;

(* Lexer rules (in uppercase) in regex *)
MNEMONIC = ? [ a-z]+ ? ;
AC_REG = ? &(0 | [1-9][0-9]*) ? ;
RF_REG = ? $(0 | [1-9][0-9]*) ? ;
LABEL_ID = ? _[a-zA-Z][a-zA-Z_]* ? ;

```

This grammar is defined using the Extended Backus-Naur Formalism (EBNF) with some terminals witted in Extended Regular Expressions (ERE) Syntax (Marked in uppercase).

### Instructions

Instructions are the basic building blocks of a program. An instruction is a command that tells the processor to perform a specific operation.

### Pseudo-Instructions

Pseudo-instructions are special commands that are used to simplify the writing of programs. They are not part of the MOOn IV ISA. The following pseudo-instructions are supported:

- call
- ret
- div
- mul
- sw
- lw

### Directives

Directives are special commands that are used to control the assembler, orientations to the assembling process. They are not part of the MOOn IV ISA. The following directives are supported:

- .include
- .data
- .text
- .word

### Labels

Labels are used to mark locations in the program. A label is a sequence of alphanumeric characters that starts with underscore and ends with a colon. For example, `_loop:` is a label.

### Pointers

A pointer is used to refer to memory locations in the program. A pointer is a sequence of alphanumeric characters that ends with a colon. For example, `vector:` is a pointer.

### Comments

Comments are used to document the program. A comment starts with a semicolon and ends at the end of the line. For example, `; This is a comment.` is a comment.