# Vaccine-Coding-Challenge

Vaccine rest api for AFFNO coding challenge using Flask.

Assumptions made -

* A person can register for many vaccination campaigns but checking if vaccine was taken or not will happen manually.
* Person gets registered for earliest available to simlify API.
* Accuracy of campaign location string is assumed.
* Vaccination occurs 24/7

Run and build instructions

* Navigate to API3
* Create virtual environment 
* pip3 install -r requirements.txt
* python3 main.py

Run test files

* python3 -m unittest test_main.Test

