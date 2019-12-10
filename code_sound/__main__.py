import sys

from .github.actions import run

if __name__ == "__main__":
    run(sys.argv[1:])
