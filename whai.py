#!/usr/bin/python3
import openai

import re
import os, sys, argparse as a




def prompt_temperature(prompt):
    # marks := '?', '!'
    most_consecutive_marks = max(map(len, re.findall(r'(\?+|!+)', prompt)))
    if most_consecutive_marks in (0, 1):
        return 0.0
    if most_consecutive_marks == 2:
        return 0.5
    if most_consecutive_marks == 3:
        return 0.7
    if most_consecutive_marks >= 4:
        return 1.0

def prompt_maxtokens(prompt):
    return 2000

def is_run_as_alias():
    return not sys.argv[0].endswith(".py")


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

    if not args.api_key:    
        args.api_key = os.getenv("OPENAI_API_KEY")

    openai.api_key = args.api_key

    service_request(args)


def service_request(args):
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



def alias_main():
    prog_name = os.path.basename(sys.argv[0])
    prompt = prog_name+" "+" ".join(sys.argv[1:])+"\n\n"

    #TODO: insert stdin and fds redirected to us into prompt

    temperature = os.environ.get("TEMPERATURE", prompt_temperature(prompt))
    max_tokens = os.environ.get("TOKENS", prompt_maxtokens(prompt))
    model_name = os.environ.get("MODEL", "text-davinci-003")

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


if __name__ == "__main__":
    if is_run_as_alias():
        alias_main()
    else:
        script_main()
