def grade(x):
    if x < 59:
        return "%dk" % kyu(x)
    else:
        return "%dd" % dan(x - 59)

def dan(x):
    if x < 90:
        return 1 + (x // 10)
    else:
        return 9

def kyu(x):
    if x < 9:
        return 25 - x
    elif x < 29:
        return 16 - ((x - 9) // 2)
    elif x < 59:
        return 6 - ((x - 29) // 5)
    else:
        return 1

def max_stars(x):
    if x < 9:
        return 0
    elif x < 29:
        return 2
    elif x < 59:
        return 5
    else:
        return 10

def stars(x):
    if x < 9:
        return 0
    elif x < 29:
        return ((x - 9) % 2) + 1
    elif x < 59:
        return ((x - 29) % 5) + 1
    elif x < 149:
        return ((x - 59) % 10) + 1
    else:
        return 10
