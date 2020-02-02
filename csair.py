import ssl
import requests
import json

class Csair():
    def get_csair(a_code, d_code, date):

        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        # send request
        url = "https://b2c.csair.com/portal/flight/direct/query"
        header = {
            "sec-ch-ua": "Google Chrome 79",
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
        }
        format_date = date.replace("-", "")
        payload = {
            "depCity": d_code,
            "arrCity": a_code,
            "flightDate": format_date,
            "adultNum": "1",
            "childNum": "0",
            "infantNum": "0",
            "cabinOrder": "0",
            "airLine": 1,
            "flyType": 0,
            "international": "0",
            "action": "0",
            "segType": "1",
            "cache": 1,
            "preUrl": "",
            "isMember": ""
        }
        request = requests.post(url, data=json.dumps(payload), headers=header)

        # store file into temp
        file = open("temp/csair_temp.json", "wb")
        file.write(request.content)

        # start analysis
        response = json.loads(request.text)
        flight_list = {}

        if response["success"]:
            route_list = response["data"]["segment"][0]["dateFlight"]["flight"]
            for item in route_list:
                flight_number = item["flightNo"]
                content = {}
                airline_code = "CZ"
                airline_name = "南方航空"
                craft_type = item["plane"]

                d_city_code = ""
                d_city_name = ""
                d_airport_code = item["depPort"]
                d_airport_name = ""

                a_city_code = ""
                a_city_name = ""
                a_airport_code = item["arrPort"]
                a_airport_name = ""

                # 格式化出发日期
                dd = item["depDate"]
                dd_list = list(dd)
                dd_list.insert(4, "-")
                dd_list.insert(7, "-")
                ddd = "".join(dd_list)

                # 格式化出发时间
                dt = item["depTime"]
                dt_list = list(dt)
                dt_list.insert(2, ":")
                dtt = "".join(dt_list)

                departure_date = ddd+" "+dtt

                # 格式化到达日期
                ad = item["arrDate"]
                ad_list = list(ad)
                ad_list.insert(4, "-")
                ad_list.insert(7, "-")
                add = "".join(ad_list)

                # 格式化到达时间
                at = item["arrTime"]
                at_list = list(at)
                at_list.insert(2, ":")
                att = "".join(at_list)

                arrival_date = add+" "+att

                lowest_price = 999999
                for cabin in item["cabin"]:
                    lowest_price = 999999
                    if cabin["adultPrice"] < lowest_price:
                        lowest_price = cabin["adultPrice"]

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

        return flight_list
