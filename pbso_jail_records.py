#!/usr/bin/env python
"""
    Parses jail booking data files provided by the Palm Beach Sheriff's Office.

    This script takes an XML file provided by the sheriff's office, parses it and outputs a flattened CSV file named the same as the XML file. The script is run via the command line and accepts the name of the XML file as an argument, like so:
    python pbso_jail_records.py myfilename.xml

    Author: Danny Sanchez, South Florida Sun Sentinel, dsanchez@sun-sentinel.com
"""

import sys
import csv
from termcolor import colored
from bs4 import BeautifulSoup

print("Parsing jail data file...")

try:
    filename = sys.argv[1]
except IndexError:
    print(colored("Error: Please provide a filename to parse.", "red", attrs=['reverse']))
    sys.exit()

try:
    with open(filename, 'r') as myfile:
        data = myfile.read().replace('\n', '')
        soup = BeautifulSoup("<Bookings>" + data + "</Bookings>", "xml")  # Needs a root tag added.

except OSError:
    print(colored("Error:", "red", attrs=['reverse']) + colored(" The provided file was not found.", "red"))
    sys.exit()

booking_data = soup.find_all("Booking")

item_counter = 0

csv_fieldnames = ["FullName", "birthdate", "Race", "address1", "city", "state", "zipcode", "BookingDate", "BookingTime", "BookingId", "Jacket", "InmateFirst", "InmateMiddle", "InmateLast", "InmateSuffix", "ReleaseDate", "ReleaseTime", "Gender", "ChargeCode", "ChargeDescription", "currentbond", "bondamount", "OBTS", "facility", "cell", "holdotheragencies"]

with open(filename.replace(".xml", "") + ".csv", 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_fieldnames)
    writer.writeheader()

    """
    The tag structure in the jail file is <Booking><Cases><Charges><BIO>

    The Booking tag contains biographical details. Inmates can have multiple cases and multiple charges within a case. It's a tree of one-to-manys. The BIOs all seem to be dupes, so this script just gets the first one.
    """
    for booking in booking_data:

        booking_attributes = ["FullName", "birthdate", "Race", "address1", "city", "state", "zipcode", "BookingDate", "BookingTime", "BookingId", "Jacket", "InmateFirst", "InmateMiddle", "InmateLast", "InmateSuffix", "ReleaseDate", "ReleaseTime", "Gender"]

        charge_attributes = ["ChargeCode", "ChargeDescription", "currentbond", "bondamount"]

        bio_attributes = ["OBTS", "facility", "cell", "holdotheragencies"]

        # Set an empty string to catch missing attributes in the data file.
        for attribute in booking_attributes:
            if booking.has_attr(attribute) is False:
                booking[attribute] = ""

        # Drill down into the list of cases.
        cases = booking.find_all("Cases")
        for case in cases:
            if case.has_attr("ArrestingAgency") is False:
                case["ArrestingAgency"] = ""

            # Drill down into the charges for the case.
            charges = case.find_all("Charges")
            for charge in charges:
                for attribute in charge_attributes:
                    if charge.has_attr(attribute) is False:
                        charge[attribute] = ""

                # Drill down into the bio for the case.
                bio = charge.find("BIO")  # Just get the first one

                for attribute in bio_attributes:
                    if bio.has_attr(attribute) is False:
                        bio[attribute] = ""

                writer.writerow({
                    "FullName": booking['FullName'],
                    "birthdate": booking['birthdate'],
                    "Race": booking['Race'],
                    "address1": booking['address1'],
                    "city": booking['city'],
                    "state": booking['state'],
                    "zipcode": booking['zipcode'],
                    "BookingDate": booking['BookingDate'],
                    "BookingTime": booking['BookingTime'],
                    "BookingId": booking['BookingId'],
                    "Jacket": booking['Jacket'],
                    "InmateFirst": booking['InmateFirst'],
                    "InmateMiddle": booking['InmateMiddle'],
                    "InmateLast": booking['InmateLast'],
                    "InmateSuffix": booking['InmateSuffix'],
                    "ReleaseDate": booking['ReleaseDate'],
                    "ReleaseTime": booking['ReleaseTime'],
                    "Gender": booking['Gender'],
                    "ChargeCode": charge['ChargeCode'],
                    "ChargeDescription": charge['ChargeDescription'],
                    "currentbond": charge['currentbond'],
                    "bondamount": charge['bondamount'],
                    "OBTS": bio['OBTS'],
                    "facility": bio['facility'],
                    "cell": bio['cell'],
                    "holdotheragencies": bio['holdotheragencies']
                })

        item_counter += 1

print("Number of bookings: " + "{:,}".format(item_counter))
