def pairs(value):   
    pairs = [v.split(':') for v in value.split(',')]
    return {pair[0]: pair[1] for pair in pairs}