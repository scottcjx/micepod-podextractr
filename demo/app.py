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
import uuid
import time
import democfg

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

print(f'waiting for {address} to be paired')

print("connecting...")

print("connected")

print("Sending notification to the device...")

c = democfg.DEMO_ITER
for _ in range(c):
    time.sleep(democfg.DEMO_DELAY/1000)
    print(f"Total Packets Recieved: {_*50} ? empty counter: 0")

print(f"Total Packets Recieved: {(c+1)*50} ? empty counter: 48")

print("end of transmission")
print("end of transmission - sys")
