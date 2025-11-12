class Suggestion():
    """Defines an event or outfit suggestion.
    Can take in a measurement of temp, wind speed, humidity, etc. and tell if the suggestion is valid"""
    
    def __init__(self, name, message):
        self.name = name        # The name of the event (e.g. "sweater")
        self.message = message  # A detaied message for the user (e.g. "Better bring a sweater.")
        self.bounds = {}        # The bounds in which the suggstion is valid (e.g. "temp" : (20,60) would indicate that this suggestion is valid if the temperature is between 20-60 degrees)
        self.precipitation = [] # The precipitation conditions under which a suggestion is valid (e.g. ["clear","cloudy"])

    def check_bound(self, category, value):
        """Check if the given value is within the bounds of the specified category"""
        return self.bounds[category][0] <= value <= self.bounds[category][1]

    def check_precipitation(self, value):
        """Check if the given precipitation is valid for this suggestion"""
        return value in self.precipitation
