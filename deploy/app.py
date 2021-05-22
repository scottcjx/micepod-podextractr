#!/usr/bin/env python3
'''
File:               podExtractr.py
Copyright           Copyright (c) 2020, Scott CJX. All Rights Reserved
Author              Scott CJX.
Version             2.0
Date                28 Oct 2020
Please refer to README.txt for instructions on operation of script
'''


# Python Default Libraries
import asyncio
import uuid
import logging
import os
import json
import sys

# Bluetooth Library
from bleak import BleakClient

# Variable declaration
# Maximum packets
empty_packet = "f" * 247
const_Total_Packets = 34111             # Total number of packets that will be transmitted from pod
const_EOF_EMPTY_COUNT = 400
r = 1

SVC_UUID = uuid.UUID("AAAAB3FC-1595-4F6A-80F0-FE094CC2AAAA")            # Service UUID for Mice Pods
RX_CHAR_UUID = uuid.UUID("0000DD58-57CE-4E7A-8E87-7CCCDDA20000")        # UUID of Characteristic that uploads data

macBuffer1 = input("Mac First 2 index ie. aa: ").lower()                # Getting User input for pod Cohort
macBuffer2 = str(input("Pod number: "))                                 # Getting User input for pod id

# Parsing Pod Cohort and Id into MAC Addresses
m_arr = list(f'{macBuffer2.zfill(10)}')
m1 = macBuffer1
m2 = m_arr[0] + m_arr[1]
m3 = m_arr[2] + m_arr[3]
m4 = m_arr[4] + m_arr[5]
m5 = m_arr[6] + m_arr[7]
m6 = m_arr[8] + m_arr[9]

address = f'{m1}:{m2}:{m3}:{m4}:{m5}:{m6}'
print(address)

# if str(input("confirm y/N: ")).lower() == 'n':                      # Getting Users confirmation of POD ID
#     raise Exception('abort')                                        # Stops program

if not os.path.exists('./data'):                                    # Creates ./data folder if not exists
    os.makedirs('./data')

with open("./data/tmp.json", 'w') as foo:
    pass


async def run(loop):

    print(f"Connecting to the device... (address: {address})")

    async with BleakClient(address, loop=loop) as client:           # Initailize Connection to client

        print(f'waiting for {address} to be paired')

        #WAITING FOR USER TO CONFIRM THAT POD HAS BEEN CONNECTED TO COMPUTER VIA SETTINGS
        input("Press enter when pod is paired")

        if await client.is_connected():
            new_json = {
                "empty_packet_counter": 0,
                "total_counter": 0
            }
            with open("./data/tmp.json", 'w') as foo:
                json.dump(new_json, foo)


            fPath = f'./data/{address.replace(":", "")}'            # Creates Pods Individual Folder if not exist

            if not os.path.exists(fPath):
                os.makedirs(fPath)

            path = f'./{fPath}/log-{address.replace(":", "")}.log'   # Creates log file for pod
            with open(path, "w") as foo:
                pass

            print("Sending notification to the device...")

            def notifyCallback(sender, data):                       # Callback Function for RX CMD
                # with open("./data/tmp.json", 'r') as foo:
                #     info = json.load(foo)
                #
                # total_packets_recieved = int(info["total_counter"])
                # empty_counter = int(info["empty_packet_counter"])
                #
                # total_packets_recieved += 1
                # is_empty = empty_packet in data.hex()

                # if (total_packets_recieved % 50 == 0) or (total_packets_recieved < 100):
                #     print(f"Total Packets Recieved {total_packets_recieved}, ?empty_counter: {empty_counter}")
                print(data.hex())
                with open(path, "a") as foo:
                    foo.write(data.hex() + '\n')                    # Appends Packet into ONE line of log file and starts newline

                # if is_empty:
                #     empty_counter += 1
                # else:
                #     empty_counter = 0
                #     r = 1
                #
                # if empty_counter > const_EOF_EMPTY_COUNT:
                #     print("end of transmission")
                #     with open(path, "a") as foo:
                #         foo.write('EOF')
                #     sys.exit("end of transmission - sys")
                # else:
                #     jsonD = {
                #         "empty_packet_counter": str(empty_counter),
                #         "total_counter": str(total_packets_recieved)
                #     }
                #     with open("./data/tmp.json", "w") as foo:
                #         json.dump(jsonD, foo)

            await client.start_notify(RX_CHAR_UUID, notifyCallback)     # Send Notify

            print("Sending TX char")
            message = bytearray(0x00)
            await client.write_gatt_char(RX_CHAR_UUID, message, True)   # Send RX CMD

            while r:
                # print("Waiting...")
                def RX_dataCallback(sender, data):
                    print(f"RX Callback Recieved: {data.hex()}")

                await client.read_gatt_char(RX_CHAR_UUID)
        else:
            raise Exception("Device not connected")


if __name__ == '__main__':
# try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    print('Press enter to exit')
    input()
