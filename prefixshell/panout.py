# -*- coding: utf-8 -*-
import logging
from prefixshell.pipeline import Pipeline


logger = logging.getLogger(__name__)


class Panout(object):

    def __init__(self, pipelines=None):
        self.pipelines = pipelines or []

    @classmethod
    def from_file(cls, filename):
        with file(filename) as f:
            pipelines = [Pipeline.build_from_cmdline(cmdline)
                         for cmdline in f]
            return cls(pipelines)

    def run(self, inp):
        pipelines = self.pipelines
        try:
            for pipeline in pipelines:
                pipeline.activate()

            for line in inp:
                for pipeline in pipelines:
                    pipeline.write(line)
            logger.info('shutdowning...')
        finally:
            for pipeline in pipelines:
                pipeline.shutdown()


def main():
    import sys

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    rcfile = sys.argv[1]

    panout = Panout.from_file(rcfile)
    panout.run(sys.stdin)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
