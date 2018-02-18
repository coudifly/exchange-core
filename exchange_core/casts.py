def pairs(value):   
    pairs = [v.split(':') for v in value.split(',')]
    try:
        return {pair[0]: pair[1] for pair in pairs}
    except IndexError:
        return {}