class SchemaError(AssertionError): pass

def validate(instance, schema, path='$'):
    expected = schema.get('type')
    if expected == 'object':
        if not isinstance(instance, dict): raise SchemaError(path + ' expected object')
        properties = schema.get('properties', {})
        required = set(schema.get('required', []))
        if set(instance) != required: raise SchemaError(path + ' keys mismatch')
        if schema.get('additionalProperties') is False and not set(instance) <= set(properties): raise SchemaError(path + ' unknown fields')
        for key, value in instance.items(): validate(value, properties[key], path + '.' + key)
    elif expected == 'array':
        if not isinstance(instance, list): raise SchemaError(path + ' expected array')
        for index, value in enumerate(instance): validate(value, schema.get('items', {}), f'{path}[{index}]')
    elif expected == 'string' and not isinstance(instance, str): raise SchemaError(path + ' expected string')
    elif expected == 'boolean' and not isinstance(instance, bool): raise SchemaError(path + ' expected boolean')
    elif expected == 'integer' and (not isinstance(instance, int) or isinstance(instance, bool)): raise SchemaError(path + ' expected integer')
    elif expected == 'number' and (not isinstance(instance, (int, float)) or isinstance(instance, bool)): raise SchemaError(path + ' expected number')
    elif expected == 'null' and instance is not None: raise SchemaError(path + ' expected null')
    return True
