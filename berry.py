berryList = {
    "oran": [16, {
        "spicy" = 10,
        "dry" = 10,
        "sweet" = 0,
        "bitter" = 10,
        "sour" = 10
    }],
    "cheri": [20],
    "pecha": [20],
    "chesto": [20],
    "rawst": [80],
    "aspear": [80],
    "persim": [80]
}

class Berry(object):
    def __init__(self, name):
        info = berryList[name]
        self.ripeTime = info[0]
        self.tastes = info[1]
