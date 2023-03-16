
from flask import Flask, request
from datetime import datetime
from Campaign import Campaign
from Appointment import Appointment

# list to store all created campaign objects
data = []

app = Flask(__name__)


@app.route('/')
def start():
    return "REST API"

#add concurency so that multiple requests can happen

# function to check json object formatting
def checkJson(campaign):
    date = campaign.date
    numDocs = campaign.numDoctors
    startTime = campaign.startTime
    endTime = campaign.endTime

    if date <= datetime.now().date():
        return "Date has passed"
    elif numDocs <= 0 or numDocs > 100:
        return "Invalid Number of doctors"
    elif endTime <= startTime:
        return "Invalid Times"
    elif CheckCampaignAvailability(campaign):
        return "The date requested already has a vaccine campaign"
    else:
        return "OK"


# Check if campaign already exists in list
def CheckCampaignAvailability(campaign):
    for camp in data:
        if camp.date == campaign.date and camp.location == campaign.location:
            return 1
    return 0


# Create campaign based on json input ibject
@app.route('/api/addCampaign', methods=['POST'])
def add():
    location = request.json['location']
    date = datetime.strptime(request.json['date'], '%Y/%m/%d').date()
    numDocs = request.json['numberOfDoctors']
    startTime = request.json['startTime']
    endTime = request.json['endTime']
    if startTime[-2:] != "AM" and startTime[-2:] != "PM":
        return "Incorrect formatting for time"
    if endTime[-2:] != "AM" and endTime[-2:] != "PM":
        return "Incorrect formatting for time"
    newC = Campaign(location, date, numDocs, startTime, endTime)
    check = checkJson(newC)
    if check != "OK":
        return check
    # add successfully created campaign to list
    data.append(newC)

    return f"Campaign on {newC.date} at {newC.location} starts at {newC.startTime}"


# check is there is a campaign on requested date
def checkAvailability(date):
    if date < datetime.now().date():
        return False
    for campaign in data:
        if date == campaign.date:
            return True

    return False


# book vaccination appointment if data input is valid
def addAppointment(campaign, appointment):
    # Check if bookable
    if appointment.nic not in campaign.appointments:
        campaign.appointments[appointment.nic] = appointment
        return "registered"
    else:
        return "Double book"


# api call for registering based on nic
@app.route('/api/register', methods=['POST'])
def register():
    date = datetime.strptime(request.json['date'], '%Y/%m/%d').date()
    location = request.json['location']
    nic = request.json['nic']
    if checkAvailability(date):
        index = addToCampaign(date, location)
        if index is None:
            return "Location not available"
        newAppoint = Appointment(location, date, nic)
        regStatus = addAppointment(data[index], newAppoint)
        if regStatus == "registered":
            data[index].appointments[nic].time = data[index].checkNextTime()  # Check time
            return f"Registered {nic} for {data[index].appointments[nic].time}"
        else:
            return regStatus
    # if there is no campaign on requested date and location
    else:
        return "unavailable"


# api call to delete registered nic
@app.route('/api/delete', methods=['DELETE'])
def delete():
    date = datetime.strptime(request.json['date'], '%Y/%m/%d').date()
    location = request.json['location']
    nic = request.json['nic']
    for campaign in data:
        # Check if deletion is valid
        if campaign.date == date and campaign.location == location and nic in campaign.appointments.keys():
            try:
                # Make time available again
                campaign.queue[campaign.appointments[nic].time] += 1
                deletedNIC = campaign.appointments.pop(nic)
            except Exception as e:
                return "{} already deleted".format(e)
            return f"Person {nic} has been deleted"
    return "nic does not exist"


# Get details about all available campaigns
@app.route('/api/getCampaigns', methods=['GET'])
def getCamp():
    output = []
    for camp in data:
        camp_data = {'date': camp.date, 'location': camp.location,
                     'numDocs': camp.numDoctors, 'time': str(camp.startTime)}
        output.append(camp_data)
    return {"Current Campaigns": output}


# get nics of all registered persons
@app.route('/api/getAppointments', methods=['GET'])
def getAppoints():
    date = datetime.strptime(request.json['date'], '%Y/%m/%d').date()
    location = request.json['location']
    output = []
    for camp in data:
        if camp.date == date and camp.location == location:
            output = str(camp.appointments.keys())
    return {"Appointments": output}


# get index of campaign based on date and location
def addToCampaign(date, location):
    for i in range(len(data)):
        if date == data[i].date and location == data[i].location:
            return i
    return None


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
