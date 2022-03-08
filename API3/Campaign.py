
from datetime import datetime, date, timedelta


#Convert time string to a datetime.time object in 24 hour clock format
def convert24(time):
    try:
        if time[-2:] == "AM":
            if time[:2] == "12":
                tempMidnight = time.replace(time[:-2], "00")
                time = tempMidnight
            if "." in time:
                time = time[:-2]
                temp = time.split('.')
                hour = temp[0]
                minute = temp[1]
                return datetime.strptime(hour + "-" + minute, '%H-%M').time()
            else:
                hour = time.strip("AM")
                minute = "00"
            return datetime.strptime(hour + "-" + minute, '%H-%M').time()

        elif time[-2:] == "PM":
            if "." in time:
                time = time[:-2]
                temp = time.split('.')
                if int(temp[0]) < 12:
                    hour = str(int(temp[0]) + 12)
                else:
                    hour = temp[0]
                minute = temp[1]
                return datetime.strptime(hour + "-" + minute, '%H-%M').time()
            else:
                if int(time.strip("PM")) < 12:
                    hour = str(int(time.strip("PM")) + 12)
                    minute = "00"
                else:
                    hour = time.strip("PM")
                    minute = "00"
            return datetime.strptime(hour + "-" + minute, '%H-%M').time()
    except Exception as e:
        return "fail{}".format(e)


# set duration of vaccination campaign
def setDuration(start, end):
    diff = datetime.combine(date.today(), end) - datetime.combine(date.today(), start)
    return diff.total_seconds()


# set number of time slots available
def setTimeSlots(duration):
    hours = duration / 3600
    slots = hours * 4
    return slots


# create schedule in 15 minute increments
def createSchedule(startTime, endTime):
    spacing = 15  # in minutes
    lst = [str(i * timedelta(minutes=spacing)) for i in range(24 * 60 // spacing)]

    timeList = []
    schedule = []

    for time in lst:
        hour = time.split(':')[0]
        minute = time.split(':')[1]
        timeList.append(datetime.strptime(hour + ":" + minute, '%H:%M').time())

    for time in timeList:
        if startTime <= time < endTime:
            schedule.append(time)

    return schedule


# create vaccination campaign queue based on numdoctors
def createQueue(numDoctors, schedule):
    queue = {}

    perSlot = numDoctors

    for time in schedule:
        queue[time] = perSlot

    return queue


# vaccination campaign class
class Campaign:

    def __init__(self, location, dateC, numDoctors, startTime, endTime):
        self.location = location
        self.date = dateC
        self.numDoctors = numDoctors
        self.startTime = convert24(startTime)
        self.endTime = convert24(endTime)
        # duration of campaign in seconds
        self.duration = setDuration(self.startTime, self.endTime)
        # number of 15 minute time slots available
        self.timeSlots = setTimeSlots(self.duration)
        # schedule in 15 minute increments
        self.schedule = createSchedule(self.startTime, self.endTime)
        # queue based on number of doctors available
        self.queue = createQueue(self.numDoctors, self.schedule)
        self.appointments = {}

    # get next available time from appointment queue
    def checkNextTime(self):
        for time in self.queue:
            if self.queue[time] > 0:
                self.queue[time] -= 1
                return time

        return "Fully Booked"
