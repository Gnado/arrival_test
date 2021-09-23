import random
import string


class DataGenerator:

    @staticmethod
    def bear_name(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def bear_age(low=0.0, high=1.0, size=1):
        return round(random.uniform(low, high), size)
