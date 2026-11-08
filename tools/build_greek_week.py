"""Compatibility entry point: Greek lessons are hand-authored canonical JSON, not scaffolds.
The original generator overwrote edited lessons and invented excerpt wording. It is retired.
"""
from content_pipeline import main


if __name__ == '__main__':
    print('Greek Week 1 generation is retired. Checking canonical content without writes.')
    main(check_only=True)
