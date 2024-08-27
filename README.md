# SEA-IV

SEA-IV - Syntax-Encoding Assembler for MOOn-IV is a simple assembler for the MOOn-IV architecture. In this repository, you will find the source code for the assembler and the documentation for the MOOn-IV assembly language in this very README file.

## MOOn-IV Assembly Language

The MOOn-IV assembly language is a low-level programming language that is used to write programs for the MOOn-IV. The MOOn IV assembly language is a human-readable representation of the machine code that is executed by the MOOn IV processor.

### Language Elements

The MOOn-IV assembly language has instructions, pseudo-instructions, directives, labels and comments.

#### Instructions

Instructions are the basic building blocks of a program. An instruction is a command that tells the processor to perform a specific operation. The MOOn-IV

#### Pseudo-Instructions

Pseudo-instructions are special commands that are used to simplify the writing of programs. They are not part of the MOOn IV ISA. The following pseudo-instructions are supported:

- jump
- lw
- sw
- mul
- div
- swap
- call
- ret

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
inst = rTypeInst | iTypeInst | sTypeInst | jTypeInst | e1TypeInst | e2TypeInst | e3TypeInst | e4TypeInst | pseudoInst;

nTypeInst = MNEMONIC ;
rTypeInst = MNEMONIC, AC_REG, ",", RF_REG, ",", RG_REG ;
iTypeInst = MNEMONIC, AC_REG, ",", NUMBER ;
sTypeInst = MNEMONIC, AC_REG, ",", RF_REG, ",", NUMBER ;
jTypeInst = MNEMONIC, NUMBER ;

e1TypeInst = MNEMONIC, AC_REG, ",", RF_REG ;
e2TypeInst = MNEMONIC, RF_REG ;
e3TypeInst = MNEMONIC, AC_REG ;
e4TypeInst = MNEMONIC, RF_REG ;

pseudoInst = jump | mul | div | swap | lw | sw ;
jump = "jump", (LABEL | NUMBER) ;
mul = "mul", RF_REG, ",", RG_REG ;

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

##### Not Use All Fields in R-type Instructions

Some R-type instructions don't use all available fields. For example, the `not` instruction only uses the a AC register and only one RF register. The syntax for these instructions is defined as follows:

| Type | Fields | Syntax |
|-|-|-|
| E1 | Only AC register and RF1 is pointed, RF2 is not used | `MNEMONIC, AC_REG, ",", RF_REG` |
| E2 | Only RF2 is pointed | `MNEMONIC, RF_REG` |
| E3 | Only AC register is pointed and RF1, RF2 is not used | `MNEMONIC, AC_REG` |
| E4 | Only RF1 is pointed | `MNEMONIC, RF_REG` |

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

- jr
- jral

##### Pseudo-Instructions Syntax

Pseudo-instructions are special commands that are used to simplify the writing of programs. They are not part of the MOOn IV ISA. The following pseudo-instructions are supported:

- jump
- lw
- sw
- mul
- div
- swap
- call
- ret

The syntax for these instructions is defined as follows:

| Pseudo-Instruction | Syntax |
|-|-|
| jump | `jump, (LABEL \| NUMBER)` |
| lw | `lw, AC_REG, ",", LABEL, "[", NUMBER, "]"` |
| sw | `sw, AC_REG, ",", LABEL, "[", NUMBER, "]"` |
| mul | `mul, RF_REG, ",", RG_REG` |
| div | `div, RF_REG, ",", RG_REG` |
| swap | `swap, RF_REG, ",", RG_REG` |
| call | `call, LABEL` |
| ret | `ret` |

<!-- todo: complete -->
<!--  ## Structure of the Assembler -->

## Installation

First, clone the repository. Second, install Python 3 Interpreter. After that, you can run the assembler using the following command in the `src` directory:

```bash
python3 main.py
```

You will need to change the `main.py` file to put the directory of the file you want to assemble. This is a temporary solution and will be fixed in the future.

<!-- todo: complete -->
<!-- ## Usage -->
