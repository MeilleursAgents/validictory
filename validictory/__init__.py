#!/usr/bin/env python

from validictory.validator import (
    FieldValidationError,
    FieldsValidationError,
    SchemaError,
    SchemaValidator,
    ValidationError
)
__all__ = [
    'FieldValidationError',
    'FieldsValidationError',
    'SchemaError',
    'SchemaValidator',
    'validate',
    'ValidationError',
]
__version__ = '0.9.1'


def validate(data, schema, validator_cls=SchemaValidator,
             format_validators=None, required_by_default=True,
             blank_by_default=False, disallow_unknown_properties=False,
             raise_at_first_error=True):
    '''
    Validates a parsed json document against the provided schema. If an
    error is found a :class:`ValidationError` is raised.

    If there is an issue in the schema a :class:`SchemaError` will be raised.

    :param data:  python data to validate
    :param schema: python dictionary representing the schema (see
        `schema format`_)
    :param validator_cls: optional validator class (default is
        :class:`SchemaValidator`)
    :param format_validators: optional dictionary of custom format validators
    :param required_by_default: defaults to True, set to False to make
        ``required`` schema attribute False by default.
    :param disallow_unknown_properties: defaults to False, set to True to
        disallow properties not listed in the schema definition
    :param raise_at_first_error: defaults to True, set to False if you want
       to bufferize errors and treat them later.
    '''
    v = validator_cls(format_validators, required_by_default, blank_by_default,
                      disallow_unknown_properties, raise_at_first_error)
    return v.validate(data, schema)

if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            raise SystemExit("%s SCHEMAFILE [INFILE]" % (sys.argv[0],))
        schemafile = open(sys.argv[1], 'rb')
        infile = sys.stdin
    elif len(sys.argv) == 3:
        schemafile = open(sys.argv[1], 'rb')
        infile = open(sys.argv[2], 'rb')
    else:
        raise SystemExit("%s SCHEMAFILE [INFILE]" % (sys.argv[0],))
    try:
        obj = json.load(infile)
        schema = json.load(schemafile)
        validate(obj, schema)
    except ValueError as e:
        raise SystemExit(e)
