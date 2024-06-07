# SEA-M

SEA-M - Syntax-Encoding Assembler for MOOn-IV is a simple assembler for the MOOn-IV architecture. It is written in Python 3 and is a command-line tool.

## MOOn-IV Assembly Language

The MOOn-IV assembly language is a low-level programming language that is used to write programs for the MOOn-IV. The MOOn IV assembly language is a human-readable representation of the machine code that is executed by the MOOn IV processor.

### Grammar

The grammar of the MOOn-IV assembly language is defined as follows:

```EBNF

asmCode = [dataField], [textField] ;

dataFIeld = ".data", dataList ;
dataList = (data | labelDec data), [dataList] ;
data = word ;

word = ".word", NUMBER {"," NUMBER} ;

textField = ".text", instList ;
instList = (inst | labelDec inst), [instList] ;
inst = rTypeInst ;

rTypeInst = MNEMONIC, AC_REG, ",", RF_REG, ",", RG_REG ;

labelDec = LABEL, ':' ;

(* Lexical rules (in uppercase) in regex *)
NUMBER = ? 0|[1-9][0-9]* ? ;
MNEMONIC = ? [a-z]+ ? ;
AC_REG = ? &(0|[1-9][0-9]*) ? ;
RF_REG = ? $(0|[1-9][0-9]*) ? ;
LABEL = ? _[a-z0-9_]* ? ;

```

This grammar is defined using the Extended Backus-Naur Formalism (EBNF) with some terminals witted in Extended Regular Expressions (ERE) Syntax.

### Language Element

The MOOn-IV assembly language has instructions, pseudo-instructions, directives, labels and comments.

#### Instructions

Instructions are the basic building blocks of a program. An instruction is a command that tells the processor to perform a specific operation. The MOOn-IV

#### Pseudo-Instructions

Pseudo-instructions are special commands that are used to simplify the writing of programs. They are not part of the MOOn IV ISA. The following pseudo-instructions are supported:

- div
- mul

#### Directives

Directives are special commands that are used to control the assembler, orientations to the assembling process. They are not part of the MOOn IV ISA. The following directives are supported:

- .include
- .data
- .ascii
- .word
- .text

#### Labels

Labels are used to mark locations in the program. A label is a sequence of alphanumeric characters that starts with underscore and ends with a colon. For example, `_loop:` is a label.

##### Comments

Comments are used to document the program. A comment starts with a semicolon and ends at the end of the line. For example, `; This is a comment.` is a comment.

<!-- todo: complete -->
## Structure of the Assembler

## Installation

## Usage
