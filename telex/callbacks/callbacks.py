from enum import Enum, unique
from inspect import signature, Parameter
from functools import partial

def _verify_signature(func, *, keywords=None):
    from inspect import signature, Parameter
    sig = signature(func)
    missing_keywords = []
    for name in keywords:
        param = sig.parameters.get(name, None)
        if not param or param.kind != Parameter.KEYWORD_ONLY:
            missing_keywords.append(name) 
    if missing_keywords:
        raise SyntaxError('"{}: {}" missiong kwonly arg(s): {}'.format(func.__module__, func.__qualname__, ', '.join(missing_keywords)))

@unique
class _CallbackKind(str, Enum):
    _MSG_RECEIVED = '_telex_callback_msgreceived'

MSG_RECEIVED = _CallbackKind._MSG_RECEIVED

_validate_signature = {}
_validate_signature[MSG_RECEIVED] = partial(_verify_signature, keywords=['msg'])


def callback(kind:_CallbackKind):
    def _callback(func):
        setattr(func, '_telex_validate_signature', _validate_signature[kind])
        setattr(func, '_telex_callback', _CallbackKind(kind))
        return func
    return _callback

