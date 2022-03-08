
from unittest import TestCase

import requests


# Class to conduct automated testing for basic functionality
class Test(TestCase):
    # Api URLs
    API_URl = "http://localhost:8080/"
    add_URL = "{}/api/addCampaign".format(API_URl)
    register_URL = "{}/api/register".format(API_URl)
    delete_URL = "{}/api/delete".format(API_URl)
    get_camp_URL = "{}/api/getCampaigns".format(API_URl)
    get_address_URL = "{}/api/getAppointments".format(API_URl)
    # Json objects
    Campaign_Obj = {
        "location": "colombo 1",
        "date": "2021/9/25",
        "numberOfDoctors": 3,
        "startTime": "2.30AM",
        "endTime": "3.30AM"
    }

    Register_Obj = {
        "location": "colombo 1",
        "date": "2021/9/25",
        "nic": "912742882ve"
    }

    Delete_Obj = {
        "location": "colombo 1",
        "date": "2021/09/25",
        "nic": "912742882ve"
    }

    Get_Appointments_Obj = {
        "location": "colombo 1",
        "date": "2021/09/25"
    }

    # test creating vaccination campaign
    def test_add(self):
        req = requests.post(Test.add_URL, json=Test.Campaign_Obj)
        self.assertEqual(req.status_code, 200)

    # test vaccine appointment registration
    def test_register(self):
        register = requests.post(Test.register_URL, json=Test.Register_Obj)
        self.assertEqual(register.status_code, 200)

    # test appointment deletion
    def test_delete(self):
        delete = requests.delete(Test.delete_URL, json=Test.Delete_Obj)
        self.assertEqual(delete.status_code, 200)

    # test getting all campaign data
    def test_get_camp(self):
        camps = requests.get(Test.get_camp_URL)
        self.assertEqual(camps.status_code, 200)

    # test getting specific appointment data
    def test_get_appoints(self):
        appoints = requests.get(Test.get_address_URL, json=Test.Get_Appointments_Obj)
        self.assertEqual(appoints.status_code, 200)
