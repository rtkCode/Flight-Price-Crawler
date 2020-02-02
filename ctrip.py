import ssl
import requests
import json

class Ctrip():
    def get_ctrip(a_code, a_city, d_code, d_city, date):

        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        # send request
        url = "https://flights.ctrip.com/itinerary/api/12808/products"
        header = {
            "sec-ch-ua": "Google Chrome 79",
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
        }
        pay_load = {
            "flightWay": "Oneway",
            "classType": "ALL",
            "hasChild": False,
            "hasBaby": False,
            "searchIndex": 1,
            "date": date,
            "airportParams": [
                {
                    "dcity": d_code,
                    "acity": a_code,
                    "dcityname": d_city,
                    "acityname": a_city,
                    "date": date,
                    "dcityid": 2,
                    "acityid": 1
                }
            ],
            # "token": "bfa66861667ef3f5087792e7be5e8c81"
        }
        request = requests.post(url, data=json.dumps(pay_load), headers=header)

        # store file into temp
        # file = open("temp/ctrip_temp.json", "wb")
        # file.write(request.content)

        # start analysis
        response = json.loads(request.text)
        flight_list = {}

        if "msg" in response:
            data = response["data"]
            route_list = data["routeList"]
            for item in route_list:
                if "flight" in item["legs"][0]:
                    flight_number = item["legs"][0]["flight"]["flightNumber"]
                    content = {}
                    airline_code = item["legs"][0]["flight"]["airlineCode"]
                    airline_name = item["legs"][0]["flight"]["airlineName"]
                    craft_type = item["legs"][0]["flight"]["craftTypeName"]

                    d_city_code = item["legs"][0]["flight"]["departureAirportInfo"]["cityTlc"]
                    d_city_name = item["legs"][0]["flight"]["departureAirportInfo"]["cityName"]
                    d_airport_code = item["legs"][0]["flight"]["departureAirportInfo"]["airportTlc"]
                    d_airport_name = item["legs"][0]["flight"]["departureAirportInfo"]["airportName"]

                    a_city_code = item["legs"][0]["flight"]["arrivalAirportInfo"]["cityTlc"]
                    a_city_name = item["legs"][0]["flight"]["arrivalAirportInfo"]["cityName"]
                    a_airport_code = item["legs"][0]["flight"]["arrivalAirportInfo"]["airportTlc"]
                    a_airport_name = item["legs"][0]["flight"]["arrivalAirportInfo"]["airportName"]

                    departure_date = item["legs"][0]["flight"]["departureDate"]
                    arrival_date = item["legs"][0]["flight"]["arrivalDate"]
                    lowest_price = item["legs"][0]["characteristic"]["lowestPrice"]

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

        # print(flight_list)
        return flight_list
