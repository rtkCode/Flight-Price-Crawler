import ssl
import requests
import json

class Ch():
    def get_ch(a_city, d_city, date):

        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        # send request
        url = "https://flights.ch.com/Flights/SearchByTime"
        header = {
            "sec-ch-ua": "Google Chrome 79",
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
        }
        form_data = {
            "Active9s": "",
            "IsJC": False,
            "IsShowTaxprice": False,
            "Currency": 0,
            "SType": 0,
            "Departure": d_city,
            "Arrival": a_city,
            "DepartureDate": date,
            "ReturnDate": None,
            "IsIJFlight": False,
            "IsBg": False,
            "IsEmployee": False,
            "IsLittleGroupFlight": False,
            "SeatsNum": 1,
            "ActId": 0,
            "IfRet": False,
            "IsUM": False,
            "CabinActId": None,
            "SpecTravTypeId": "",
            "IsContains9CAndIJ": False,
            "isdisplayold": False
        }
        request = requests.post(url, data=json.dumps(form_data), headers=header)

        # store file into temp
        file = open("temp/ch_temp.json", "wb")
        file.write(request.content)

        # start analysis
        response = json.loads(request.text)
        flight_list = {}
        min_price = response["MinPrice"]
        flight_list["minPrice"]=min_price

        route_list = response["Route"]
        for item in route_list:
            flight_number = item[0]["No"]
            content = {}
            airline_code = "9C"
            airline_name = "春秋航空"
            craft_type = item[0]["Type"]

            d_city_code = item[0]["DepartureCode"]
            d_city_name = item[0]["Departure"]
            d_airport_code = item[0]["DepartureAirportCode"]
            d_airport_name = item[0]["DepartureStation"]

            a_city_code = item[0]["ArrivalCode"]
            a_city_name = item[0]["Arrival"]
            a_airport_code = item[0]["ArrivalAirportCode"]
            a_airport_name = item[0]["ArrivalStation"]

            departure_date = item[0]["DepartureTime"]
            arrival_date = item[0]["ArrivalTime"]
            lowest_price = item[0]["MinCabinPrice"]

            content["airlineCode"] = airline_code
            content["airlineName"] = airline_name
            content["craft_type"] = craft_type

            content["dCityCode"] = d_city_code
            content["dCityName"] = d_city_name
            content["dAirportCode"] = d_airport_code
            content["dAirportName"] = d_airport_name

            content["aCityCode"] = a_city_code
            content["aCityName"] = a_city_name
            content["aAirportCode"] = a_airport_code
            content["aAirportName"] = a_airport_name

            content["departureDate"] = departure_date
            content["arrivalDate"] = arrival_date
            content["lowestPrice"] = lowest_price

            flight_list[flight_number] = content

        print(flight_list)
        return flight_list
