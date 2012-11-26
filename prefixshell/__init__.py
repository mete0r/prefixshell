# -*- coding: utf-8 -*-
import os
import sys
import shlex
from prefixshell.pipeline import Pipeline


def main():
    import readline
    readline.parse_and_bind('')

    prefix = sys.argv[1:]
    stack = []
    while True:
        try:
            prompt = '$ %s ' % (' '.join(prefix + stack))
            cmdline = raw_input(prompt)
        except EOFError:
            sys.stderr.write(os.linesep)
            if len(stack) == 0:
                return 0
            else:
                stack.pop()
        else:
            tokens = shlex.split(cmdline)
            if len(tokens) > 0 and tokens[0] == '+':
                stack.extend(tokens[1:])
                continue
            pipeline = Pipeline.build_from_tokens(prefix + stack + tokens)
            pipeline.activate()
            pipeline.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
