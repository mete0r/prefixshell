# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)


class Pipeline(object):

    def __init__(self, pipeline, to_write=None):
        self.pipeline = pipeline
        self.to_write = to_write
        self.subprocs = []
        self.stdin_to_frontend = None

    @classmethod
    def build_from_cmdline(cls, cmdline):
        return cls(*cls.parse_cmdline(cmdline))

    @classmethod
    def build_from_tokens(cls, tokens):
        return cls(*cls.parse_tokens(tokens))

    @classmethod
    def parse_cmdline(cls, cmdline):
        import shlex
        tokens = shlex.split(cmdline)
        return cls.parse_tokens(tokens)

    @classmethod
    def parse_tokens(cls, tokens):
        assert len(tokens) > 0

        to_write = None
        pipeline = []

        if len(tokens) >= 2 and tokens[-2] in ('>', '>>'):
            filename = tokens[-1]
            mode = {'>':'w','>>':'a'}[tokens[-2]]
            to_write = filename, mode
            tokens = tokens[:-2]

        cmd = []
        while len(tokens) > 0:
            tok, tokens = tokens[0], tokens[1:]
            if tok == '|':
                assert len(cmd) > 0
                pipeline.append(cmd)
                cmd = []
            else:
                cmd.append(tok)
        if len(cmd) > 0:
            pipeline.append(cmd)

        return pipeline, to_write


    def activate(self):
        pipeline = list(self.pipeline)
        to_write = self.to_write

        if to_write is not None:
            final_stdout = file(*to_write)
        else:
            final_stdout = None

        from subprocess import Popen
        from subprocess import PIPE

        first = True
        while len(pipeline) > 0:

            args, pipeline = pipeline[0], pipeline[1:]

            have_next = len(pipeline) > 0

            if first:
                stdin = PIPE
            if have_next:
                stdout = PIPE
            else:
                stdout = final_stdout

            p = Popen(args, stdin=stdin, stdout=stdout, close_fds=True)
            logger.info('%s: %s', p.pid, ' '.join(x for x in args))
            self.subprocs.append(p)
            if first:
                self.stdin_to_frontend = p.stdin
                first = False
            if have_next:
                stdin = p.stdout
            else:
                if final_stdout is not None:
                    final_stdout.close()

        return self.stdin_to_frontend

    @property
    def frontend_pid(self):
        return self.subprocs[0].pid

    def write(self, line):
        logger.debug('panout to %s: %s', self.frontend_pid, line)
        self.stdin_to_frontend.write(line)

    def shutdown(self):
        if self.stdin_to_frontend:
            self.stdin_to_frontend.close()
        for p in self.subprocs:
            logger.info('waiting for shutdown %s', p.pid)
            p.wait()



