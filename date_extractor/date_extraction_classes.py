from enum import Enum

class IndicatorType(Enum):
    DATE = 0
    YEAR = 1
    MONTH = 2
    DAY = 3
    TIME = 4

# Class to store data about each token
class DateIndicator:
    def __init__(self, tok: str, position: int, time_type: IndicatorType):
        self.token: str = tok
        self.pos: int = position
        self.time_type: IndicatorType = time_type

    def check_type(self):
        print(self.time_type, type(self.time_type))
    
    def __str__(self):
        return f"({self.token}, loc: {self.pos}, time_type: '{self.time_type}')"
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        return self.time_type.value < other.time_type.value

    def __gt__(self, other):
        return self.time_type.value > other.time_type.value

    def __le__(self, other):
        return self.time_type.value <= other.time_type.value
    
    def __ge__(self, other):
        return self.time_type.value >= other.time_type.value
    
    def __eq__(self, other):
        return self.time_type.value == other.time_type.value
    
    def __ne__(self, other):
        return self.time_type.value != other.time_type.value
    
month_dict = {
    "january": "01",
    "jan": "01",
    "february": "02",
    "feb": "02",
    "march": "03",
    "mar": "03",
    "april": "04",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "june": "06",
    "jul": "07",
    "july": "07",
    "august": "08",
    "aug": "08",
    "september": "09",
    "sep": "09",
    "october": "10",
    "oct": "10",
    "november": "11",
    "nov": "11",
    "december": "12",
    "dec": "12",
}