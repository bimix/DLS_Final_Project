import random


class Randomizer():

    def __init__(self):
        self._length = 10
        self._rand_string = ""

        rand = self.randomize()
        print(rand)

    def randomize(self):
        # Generate a random string of letters, symbols and numbers with a length of 6
        for r in range(0, self._length):
            x = random.randint(0, 9)
            if x <= 3:
                # Add letters to the rand_string
                self._rand_string += str(random.choice('abcdefghijklmnopqrstuvxyz'))
            elif x <= 6:
                # Add symbols to the rand_string
                self._rand_string += str(random.choice('*|!#£$%&/()=?{[]}-<>'))
            else:
                # Add numbers to the rand_string
                self._rand_string += str(random.randrange(0, 9))

        return self._rand_string


Randomizer()
