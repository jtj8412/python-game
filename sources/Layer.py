

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


Layer = enum("Background", "BackObject", "Missile", "Default", "FrontObject", "UI", "Length")



