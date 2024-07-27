# SEA-IV

SEA-IV - Syntax-Encoding Assembler for MOOn-IV is a simple assembler for the MOOn-IV architecture. It is written in Python 3 and is a command-line tool.

## MOOn-IV Assembly Language

The MOOn-IV assembly language is a low-level programming language that is used to write programs for the MOOn-IV. The MOOn IV assembly language is a human-readable representation of the machine code that is executed by the MOOn IV processor.

### Language Elements

The MOOn-IV assembly language has instructions, pseudo-instructions, directives, labels and comments.

#### Instructions

Instructions are the basic building blocks of a program. An instruction is a command that tells the processor to perform a specific operation. The MOOn-IV

#### Pseudo-Instructions

Pseudo-instructions are special commands that are used to simplify the writing of programs. They are not part of the MOOn IV ISA. The following pseudo-instructions are supported:

#### Directives

Directives are special commands that are used to control the assembler, orientations to the assembling process. They are not part of the MOOn IV ISA. The following directives are supported:

- .include
- .data
- .space
- .word
- .ascii
- .byte
- .inst

#### Labels

Labels are used to mark locations in the program. A label is a sequence of alphanumeric characters that starts with underscore and ends with a colon. For example, `_loop:` is a label.

#### Comments

Comments are used to document the program. A comment starts with a hashtag and ends at the end of the line. For example, `# This is a comment.` is a comment.

### Grammar

The grammar of the MOOn-IV assembly language is defined as follows:

```EBNF

asmCode = {include | dataField | textField} ;

include = ".include", STRING ;

dataField = ".data", dataList ;
dataList = (data | labelDec data), [dataList] ;
data = space | word | ascii | byte ;

space = ".space", NUMBER ;
word = ".word", NUMBER {"," NUMBER} ;
byte = ".byte", NUMBER {"," NUMBER} ;
ascii = ".ascii", STRING ;

instField = ".inst", instList ;
instList = (inst | labelDec inst), [instList] ;
inst = rTypeInst ;

nTypeInst = MNEMONIC ;
rTypeInst = MNEMONIC, AC_REG, ",", RF_REG, ",", RG_REG ;

labelDec = LABEL, ':' ;

(* Lexical rules (in uppercase) in regex *)
NUMBER = ? 0|[1-9][0-9]* ? ;
STRING = ? "[^"]*" ? ;
MNEMONIC = ? [a-z]+ ? ;
AC_REG = ? &(0|[1-9][0-9]*) ? ;
RF_REG = ? $(0|[1-9][0-9]*) ? ;
LABEL = ? _[a-z0-9_]* ? ;

```

This grammar is defined using the Extended Backus-Naur Formalism (EBNF) with some terminals witted in Extended Regular Expressions (ERE) Syntax.

#### Special Syntax Instructions

Some R-type instructions don't use all available fields. For example, the `not` instruction only uses the a AC register and only one RF register. The syntax for these instructions is defined as follows:

| Type | Fields | Syntax |
|-|-|-|
| E1 | Only AC register and RF1 is pointed, RF2 is not used | `MNEMONIC, AC_REG, ",", RF_REG` |
| E2 | Only RF2 is pointed | `MNEMONIC, RF_REG` |
| E3 | Only AC register is pointed and RF1, RF2 is not used | `MNEMONIC, AC_REG` |
| E4 | By convention, the left address receives the result so, in swr, ac is on the right | `MNEMONIC, RF_REG, ",", RF_REG, ",", AC_REG` |
| E5 | Only RF1 is pointed | `MNEMONIC, RF_REG` |

The list of instructions that use these special syntaxes is as follows:

E1-type:

- not
- mtac
- mfac
- bgtzr
- bltzr
- beqzr
- bnezr

E2-type:

- tmul
- tdiv

E3-type:

- mtl
- mfl
- mth
- mfh
- pop
- push

E4-type:

- swr

E5-type:

- jr
- jral

<!-- todo: complete -->
## Structure of the Assembler

## Installation

## Usage
