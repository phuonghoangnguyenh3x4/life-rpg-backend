import random

MAX_INT = 2147483647

class randint:
    @staticmethod
    def get(seed=None, args=None):
        if seed != None:
            random.seed(seed)
        if args: 
            return random.randint(*args)
        return random.randint(0, MAX_INT)
    
print(randint.get())