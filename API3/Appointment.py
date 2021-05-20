"""
Affno Coding challenge
Rushith Karunaratne
20/05/2021
"""


# Appointment class
class Appointment:
    time = None

    def __init__(self, location, date, nic):
        self.location = location
        self.date = date
        self.nic = nic
