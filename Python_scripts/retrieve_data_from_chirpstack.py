"""
Made by : Simon BEUREL
Link of the project : https://github.com/simonbeurel/Outdoor_Cattle_Tracking_LoRaWAN
"""

import requests
from time import sleep
from flask import Flask, jsonify
import threading
from datetime import datetime, timezone
from datetime import datetime


'''
This is the main file of this project. It's a Flask server that will be used to retrieve and parse data from ChirpStak API.
'''
app = Flask(__name__)

#The RSSI value one meter away from the gateway. Useful for compute the distance between the cow and the gateway
dict_value_RSSI = {
    "DUT_Milesight": -114.5,
    "Rak7240_AS923_2_DUT": -58.5
}

#The position of the gateways. It's useful for compute the position of the cow
dict_pos_long_lat_gateways = {
    "DUT_Milesight": [16.07501, 108.15404],
    "Rak7240_AS923_2_DUT": [16.07503, 108.15404]
}

#To complete with the devEUI of others cards, it's useful for know which card is active and which card is not
#It have to be false at the initialization
# XX_name_XX : [activity, last_date, latitude, longitude]
dict_cards_EUI = {
    "d819f652884e0d04": [False, None, 16.07501, 108.15404],
    "testEUI": [False, None, 25.07501, 108.15404],
}

last_date = ""
state_cow = []

'''
This function will compute the position of the cow. It will use the RSSI value of the two gateways and the name of the two gateways.
It will return the position of the cow in a list [x, y]
'''
def compute_position(rssi_first, rssi_second, gateway_name_first, gateway_name_second):
    if gateway_name_first not in dict_value_RSSI or gateway_name_second not in dict_value_RSSI:
        return None

    print(f"GATEWAYS CALLED ARE {gateway_name_first} and {gateway_name_second}")
    distance_first_gateway = 10 ** ((dict_value_RSSI[gateway_name_first] - rssi_first) / (10 * 2))
    distance_second_gateway = 10 ** ((dict_value_RSSI[gateway_name_second] - rssi_second) / (10 * 2))

    x1 = dict_pos_long_lat_gateways[gateway_name_first][0]
    y1 = dict_pos_long_lat_gateways[gateway_name_first][1]

    x2 = dict_pos_long_lat_gateways[gateway_name_second][0]
    y2 = dict_pos_long_lat_gateways[gateway_name_second][1]

    print(f"VALUES ARE {x1}, {y1}, {x2}, {y2}, {distance_first_gateway}, {distance_second_gateway}")

    x = (distance_first_gateway ** 2 - distance_second_gateway ** 2 + x2 ** 2 - x1 ** 2 + y2 ** 2 - y1 ** 2) / (
            2 * (y2 - y1))
    y = (distance_first_gateway ** 2 - distance_second_gateway ** 2 + x2 ** 2 - x1 ** 2 + y2 ** 2 - y1 ** 2) / (
            2 * (x2 - x1))

    return [x, y]

'''
This function will detect the behavior of the cow based on the Y value of the accelerometer data.
'''
def is_moving(data):
    return abs(data[1]) > 1

'''
This function will detect if the cow is eating based on the X value of the accelerometer data.
'''
def is_eating(data):
    return abs(data[0]) > 4

'''
This function will detect the behavior of the cow based on the accelerometer data.
If the cow is not EATING of MOVING, it will return IMMOBILE
'''
def detect_behavior(data):
    if is_eating(data):
        return "EATING"
    elif is_moving(data):
        return "MOVING"
    else:
        return "IMMOBILE"

'''
This function will search the last data from the ChirpStack API and call the function parse_data to parse the data.
'''
def search_last_data(last_date):
    url = "https://api.vngalaxy.vn/api/uplink/"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZFVUkiOiJkODE5ZjY1Mjg4NGUwZDA0IiwiYXBwSUQiOiI4MCIsImVtYWlsIjoibG9uZy52dTY2MjBAZ21haWwuY29tIiwicGFzc3dvcmQiOiJMb25nMTIzQCIsImlhdCI6MTcxNTgyMjQwM30.cpXgn7q9EFXMsIfp0zyf8zHR3KHVdS_H4IPl_vNOJZ4",
        "Content-Type": "application/json"
    }
    body = {
        "limit": 1
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        data_list = response.json()['data']
        return parse_data(data_list, last_date)
    else:
        print("Erreur lors de la requête : ", response.status_code)


'''
This function will update the state of the cards. 
If a card is not sending data for more than 60 minutes, it will be considered as inactive.
'''
def update_cards_state(devEUI, date):
    dict_cards_EUI[devEUI][0] = True
    json_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    json_date = json_date.replace(tzinfo=timezone.utc)
    dict_cards_EUI[devEUI][1] = json_date

    for card in dict_cards_EUI:
        if dict_cards_EUI[card][1] is not None:
            current_time = datetime.now(timezone.utc)
            time_difference = current_time - dict_cards_EUI[card][1]
            minutes_elapsed = time_difference.total_seconds() / 60
            if minutes_elapsed > 60:
                dict_cards_EUI[card][0] = False
                print(f"[+] Card {card} is now considered as inactive")

    print(f"[+] Cards state : {dict_cards_EUI}")


'''
This function will parse the data from the ChirpStack API.
'''
def parse_data(data_list, last_date):
    objectJSON = data_list[0]['objectJSON']
    if last_date == data_list[0]['timeSystem']:
        return None
    else:
        print("[+] New data detected")

        # Check if the card is already in the dictionary, if not, add it
        if data_list[0]['devEUI'] not in dict_cards_EUI:
            dict_cards_EUI[data_list[0]['devEUI']] = [False, None, 00.00000, 00.00000]
            print(f"[+] New card detected : {data_list[0]['devEUI']}")

        update_cards_state(data_list[0]['devEUI'], data_list[0]['timeSystem'])

        for gateway in data_list[0]['rxInfo']:
            if gateway['name'] == "DUT_Milesight" or gateway['name'] == "Rak7240_AS923_2_DUT":
                #print(f"[+] Gateway from DNIIT office : {gateway['name']} -> {gateway['rssi']}")
                if gateway['name'] == "DUT_Milesight":
                    distance = 10 ** ((dict_value_RSSI['DUT_Milesight'] - gateway['rssi']) / (10 * 2))
                    #print(f"[+] Distance from DUT_Milesight : {distance} m")
                else:
                    distance = 10 ** ((dict_value_RSSI['Rak7240_AS923_2_DUT'] - gateway['rssi']) / (10 * 2))
                    #print(f"[+] Distance from Rak7240_AS923_2_DUT : {distance} m")

        # Compute the position of the cow
        #position = compute_position(data_list[0]['rxInfo'][0]['rssi'], data_list[0]['rxInfo'][1]['rssi'],
                                    #data_list[0]['rxInfo'][0]['name'], data_list[0]['rxInfo'][1]['name'])
        #print(f"[+] Position of the cow : {position}")

        return [objectJSON['acceleration_x'], objectJSON['acceleration_y'], objectJSON['acceleration_z'],
                data_list[0]['timeSystem'], data_list[0]['devEUI']]


###FLASK PART###
#This section is the Flask part of the code. There is some paths that will be used to retrieve data from the server.
@app.route('/states')
def main_page():
    return jsonify(state_cow)

@app.route('/last_date')
def last_date():
    return jsonify(last_date)

@app.route('/card_active')
def card_active():
    card_active = 0
    for card in dict_cards_EUI:
        if dict_cards_EUI[card][0] is True:
            card_active += 1
    return jsonify({"Number of actives cards": card_active})

@app.route('/card_inactive')
def card_inactive():
    card_inactive = 0
    for card in dict_cards_EUI:
        if dict_cards_EUI[card][0] is False:
            card_inactive += 1
    return jsonify({"Number of inactives cards": card_inactive})

@app.route('/geomap')
def geomap():
    geojson_list = []
    current_time = datetime.utcnow().isoformat() + 'Z'
    for device_id, data in dict_cards_EUI.items():
        activity, last_date, latitude, longitude = data
        geojson_entry = {
            "time": current_time if last_date is None else last_date,
            "latitude": latitude,
            "longitude": longitude,
            "device_id": device_id,
            "status": "active" if activity else "inactive"
        }
        geojson_list.append(geojson_entry)
    return jsonify(geojson_list)

'''
This function will fetch data from the ChirpStack API every 60 seconds.
'''
def data_fetching_loop():
    global last_date, state_cow, card_active, card_inactive, dict_cards_EUI
    while True:
        ret = search_last_data(last_date)
        if ret is not None:
            last_date = ret[3]
            print("[+] Data received: ", ret)
            state = detect_behavior(ret[:3])
            if state == "IMMOBILE" and state_cow[-1]["state"] == "IMMOBILE":
                print("The cow is in danger")
                state = "DANGER"
            print(f"[+] State of the cow : {state}")
            state_cow.append({"timestamp": last_date, "CardEUI": ret[4], "state": state})
            print(state_cow)
        else:
            print(f"No new data, last data was {last_date}")
        print("=====================================")
        sleep(60)
        
        # Reset the data before the end of the day
        now = datetime.now()
        if (now.hour == 23 and now.minute == 59) or (now.hour == 0 and now.minute == 0):
            state_cow = []
            print("Resetting state_cow list")
            sleep(60)


if __name__ == "__main__":
    # We are using a thread to fetch data from the ChirpStack API every 60 seconds and a thread to run the Flask server
    data_thread = threading.Thread(target=data_fetching_loop)
    data_thread.daemon = True
    data_thread.start()
    app.run(host='0.0.0.0', port=5000 ,debug=True)
