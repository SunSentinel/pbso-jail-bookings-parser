import sys
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

"""
The tag structure here is <Booking><Cases><Charges><BIO>

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

    booking_data = {
        "FullName": booking["FullName"],
        "birthdate": booking["birthdate"],
        "Race": booking["Race"],
        "address1": booking["address1"],
        "city": booking["city"],
        "state": booking["state"],
        "zipcode": booking["zipcode"],
        "BookingDate": booking["BookingDate"],
        "BookingTime": booking["BookingTime"],
        "BookingId": booking["BookingId"],
        "Jacket": booking["Jacket"],
        "InmateFirst": booking["InmateFirst"],
        "InmateMiddle": booking["InmateMiddle"],
        "InmateLast": booking["InmateLast"],
        "InmateSuffix": booking["InmateSuffix"],
        "ReleaseDate": booking["ReleaseDate"],
        "ReleaseTime": booking["ReleaseTime"],
        "Gender": booking["Gender"]
    }

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

    item_counter += 1

print("Number of bookings: " + "{:,}".format(item_counter))
