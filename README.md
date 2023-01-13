# ⛭ WhAI

 - Author: Supersonic Tumbleweed
 - Created: 12 Jan 2023
 - License: MIT

### Repository
 
 - https://github.com/ST92/whai

## Requirements

 - sh-like shell
 - python3
 - official openai client library ("`pip3 install openai`")

## Configuration options (in `./whai.py`)

 - Installation path (`~` will be expanded).
 - Words used to generate names during install.
 - Capitalize words?
   Setting this to `False` is not recommended due to risk of name conflict with existing binaries.
 
 - What characters to prefix all names with.
   Recommended comma `','` or empty `''`.

## Usage

 By default, these settings result in filenames like `,What`, `,Explain` and are installed into `~/.local/bin/`

 This results in usage like:

    $ ,What year marks the start of industrial revolution??
 
    <... answer to "What year marks the start of industrial revolution??" >
     $ ,Who was the first black president of United States?
    
    <... answer to "Who was the first black president of United States?" >

 in your bash compatible shell, as long as `OPENAI_API_KEY` is conigured in your environment.

### Fun!!!

 If not specified otherwise (by using `TEMPERATURE` env var), the "creativity" quotient of GPT-3 is determined as inversely proportional to the longest streak of '!' or '?' in the prompt.
 No such characters are equivalent to having one.
 Two or three are in-between values.
 Four or more mean max temperature.

 Here are some prompts with guessed temperatures:
 
    $ ,Explain basics of tree growth! (temp=0.0, strict, non-chaotic)
    $ ,Explain basics of tree growth!!! (temp=0.7, moderately creative)
    $ ,Explain basics of tree growth!!??!!!?? (temp=0.7, moderately creative)
    $ ,Explain basics of tree growth???? (temp=1.0, high chances of straight up nonsense)
 
## Installation

 Installation is optional and for convenience only. 
 To do it, run
   
    $ ./whai.py install
