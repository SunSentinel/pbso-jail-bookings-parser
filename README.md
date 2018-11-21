# Palm Beach Sheriff's Office Jail Booking Data Parser

This script parses jail booking data files provided by the Palm Beach Sheriff's Office and converts them into a flattened CSV file.

## Getting Started

This script was written for Python 3.6.5. To get started, create a [virtualenv](https://virtualenv.pypa.io/en/latest/) for your project and then install the needed libraries:

```
pip install -r requirements.txt
```

### About the data file

The intended XML data file is provided by the Palm Beach Sheriff's Office and contains records of all inmates booked by the sheriff's office. It includes biographical details about the inmate, as well as a list of charges and details about the booking, such as the arresting agency, jail facility, release information and more.

The sheriff's office XML file is structured like so:

```
<Booking FullName="MONSTER, COOKIE" birthdate="1969-11-10T00:00:00" Race="B" address1="123 SESAME ST" city="NEW YORK CITY" state="NY" zipcode="10128" BookingDate="2018-11-21T00:00:00" BookingTime="1900-01-01T00:25:34" BookingId="2018112103" Jacket="0123456" InmateFirst="COOKIE" InmateMiddle="D" InmateLast="MONSTER" InmateSuffix="" ReleaseDate="2018-11-22T00:00:00" ReleaseTime="1899-12
-30T08:32:10" Gender="M">
    <Cases ArrestingAgency="01-PBSO">
        <Charges ChargeCode="322.34-7253" ChargeDescription="MOVING TRAFFIC VIOL - DRIVING UNDER THE INFLUENCE OF EXCESSIVE COOKIES" currentbond="3000.0000" bondamount="0.0000">
            <BIO OBTS="0123456789" facility="RELEASED TO ANOTHER COUNTY" cell="" holdotheragencies="No" />
        </Charges>
    </Cases>
</Booking>
```

The script flattens the XML data to create a single row for each charge containing all the biographical details, arresting info, charge details and more.

## Authors

* **[Danny Sanchez](https://github.com/dannysanchez)**

## License

This project is licensed under the MIT License.