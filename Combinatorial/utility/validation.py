"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Validation support utilities.
"""

from inspect import stack
from pathlib import Path


def check() -> str:
    """Return formatted text for precondition checks.

    This function provides concise and consistent responses for all
    precondition asserts by extracting information from the stack.
    """
    stack_ = stack()[1]
    locals_ = stack_.frame.f_locals
    if 'self' in locals_:
        source = locals_['self'].__class__.__name__
    elif 'cls' in locals_:
        source = locals_['cls'].__name__
    else:
        # Get the module name where there is neither self nor cls.
        source = Path(stack_.filename).with_suffix('').name
    method = stack_.function
    text = ''.join(stack_.code_context)
    argument = next((n for n in locals_ if
                     n in text and n not in ('self', 'cls')), None)
    context = 'Prerequisite failed in'
    if argument:
        value = locals_[argument]
        return f'{context} {source}.{method} [{argument}={value}]'
    else:
        return f'{context} {source}.{method}'
