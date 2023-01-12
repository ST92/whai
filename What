#!/usr/bin/python3
import openai

import re
import os, sys, argparse as a

### ⛭ WhAI
#
# Author: Supersonic Tumbleweed
# Created: 12 Jan 2023
# License: MIT
#
# Repository: https://github.com/ST92/whai
#
### Requirements
#
# - sh-like shell
# - python3
# - official openai client library ("pip3 install openai")
#
### Configuration
#
# Installation path (~ will be expanded)
#
INSTALL_PATH = "~/.local/bin"
#
# Words used to generate names during install
# 
interrogatives = "what which when where who whom whose why whether how".split()
others = "explain tell say is was were will would whether may can could assuming given show create write make".split()
INSTALL_WORDS = [*interrogatives, *others]
#
# Do capitalize words? Setting this to False is not recommended (risk of name conflict with existing binaries)
#
CAPITALIZE_WORDS = True
#
# What characters to prefix all names (recommended comma ',' or empty '')
#
FILENAME_PREFIX = ","
#
# This function prepares filename during installation (by default using above two settings)
#
FILENAME_TRANSFORM = lambda word: FILENAME_PREFIX+(str(word).capitalize() if CAPITALIZE_WORDS else str(word))
#
#
# By default, these settings result in filenames like ",What", ",Explain" and are installed into ~/.local/bin/
#
# This results in usage like:
# $ ,What year marks the start of industrial revolution?
#
### Installation
#
# Installation is optional and for convenience only. To do it, run
# $ ./whai.py install
#
### //

def script_main():
    p = a.ArgumentParser(
        description="Przetwarza plik wejściowy do pliku wyjściowego, poprzez AI"
    )

    p.add_argument(
        "infile", nargs=1, type=a.FileType("r"), default=sys.stdin, metavar="plik in",
    )
    p.add_argument(
        "outfile", nargs="?", type=a.FileType("w"), default=sys.stdout, metavar="plik out",
    )
    p.add_argument(
        "--temperature", type=float, default=0.7, metavar="temperatura",
        dest="temp"
    )
    p.add_argument(
        "--tokens", type=int, default=300, metavar="tokeny",
        dest="tokens"
    )
    p.add_argument(
    "--model", type=str, default="text-davinci-003", dest="model", required=False,
    )
    p.add_argument(
    "--api-key", type=str, default="", dest="api_key", required=False,
    )

    args = p.parse_args()

    if not args.api_key: args.api_key = os.getenv("OPENAI_API_KEY")

    openai.api_key = args.api_key

    prompt_string = args.infile[0].read()
    args.infile[0].close()

    response = None
    allok = False
    try:
        response = openai.Completion.create(
        model=args.model,
        prompt=prompt_string,
        temperature=args.temp,
        max_tokens=args.tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        allok = True
    finally:
        if not allok:
            sys.exit(1)    

    response_text = response.choices[0].text # type: ignore

    args.outfile.write(response_text)
    args.outfile.write("\n")
    args.outfile.close()



def guess_prompt_temperature(prompt):
    # marks := '?', '!'
    matches = re.findall(r'(\?+|!+)', prompt)
    
    most_consecutive_marks = max(map(len, matches)) if matches else 0
    
    if most_consecutive_marks in (0, 1):
        return 0.0
    if most_consecutive_marks == 2:
        return 0.5
    if most_consecutive_marks == 3:
        return 0.7
    if most_consecutive_marks >= 4:
        return 1.0

def guess_prompt_maxtokens(prompt):
    return 2000

def alias_main():
    prog_name = os.path.basename(sys.argv[0])
    prompt = prog_name+" "+" ".join(sys.argv[1:])+"\n\n"

    #TODO: insert stdin and fds redirected to us into prompt

    temperature = os.environ.get("TEMPERATURE", guess_prompt_temperature(prompt))
    max_tokens = os.environ.get("TOKENS", guess_prompt_maxtokens(prompt))
    model_name = os.environ.get("MODEL", "text-davinci-003")
    
    openai.api_key = os.getenv("OPENAI_API_KEY", openai.api_key)

    response = None
    allok = False
    try:
        response = openai.Completion.create(
            model=model_name,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        allok = True
    finally:
        if not allok:
            sys.exit(1)
    
    response_text = response.choices[0].text # type: ignore

    print(response_text)



def install_main():
    self_path = sys.argv[0]

    install_path = os.path.expanduser(INSTALL_PATH)

    os.makedirs(install_path, exist_ok=True)
    
    print("Created links to self:")
    successfully_installed = []
    for prompting_word in INSTALL_WORDS:
        executable_word = FILENAME_TRANSFORM(prompting_word)
        
        where = os.path.join(install_path, executable_word)
        if not os.path.exists(where):
            os.link(self_path, where)
            successfully_installed.append(executable_word)
    
    print("\n".join(successfully_installed))

    path_dirs = os.get_exec_path()

    if install_path in path_dirs or INSTALL_PATH in path_dirs:
        return
    else:
        print("Installation directory doesn't seem to be currently in environment PATH.")
        


def uninstall_main():
    self_path = sys.argv[0]
    self_stat = os.stat(self_path)

    install_path = os.path.expanduser(INSTALL_PATH)

    print("Removed links to self:")
    removed = []
    for file_name in os.listdir(install_path):
        file_path = os.path.join(install_path, file_name)

        if self_path == file_path: continue

        file_stat = os.stat(file_path, follow_symlinks=False)
        if os.path.samestat(self_stat, file_stat):
            os.unlink(file_path)
            removed.append(file_name)

    print("\n".join(removed))


def is_run_as_alias():
    return not sys.argv[0].endswith(".py")

if __name__ == "__main__":
    if is_run_as_alias():
        alias_main()
    elif " ".join(sys.argv[1:]).lower() == "install":
        install_main()
    elif " ".join(sys.argv[1:]).lower() == "uninstall":
        uninstall_main()
    else:
        script_main()
    
