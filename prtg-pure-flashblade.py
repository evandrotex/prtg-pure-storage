# -*- coding: utf-8 -*-
#!/usr/bin/python

# Usage
# Setup api key as "Credentials for Script Sensors" placeholder 1 (if other position is used, change line 29).
# Use additional parameters in PRTG with format key=value (Example: scope=hardware arrayaddress=%host).

# Install requests module
# https://kb.paessler.com/en/topic/90686-i-want-to-install-python-packages-for-the-python-installation-of-prtg-how-can-i-do-that
import os,requests,json,operator,sys

# custom prtg module, run only on prtg server
# https://kb.paessler.com/en/topic/90484-what-do-i-need-to-know-about-prtg-22-2-77-regarding-python
from paesslerag_prtg_sensor_api.sensor.result import CustomSensorResult
from paesslerag_prtg_sensor_api.sensor.units import ValueUnit


###############################################################################
# PRTG parameters
###############################################################################
data = json.loads(sys.argv[1])
additional_params = data['params']
perams = dict(x.split('=') for x in additional_params.split(' '))
## Get hosts from prtg´s default placeholder
#HOST = data['host']

## Get hosts from additional parameters
HOST = perams['arrayaddress']
API_TOKEN = data['scriptplaceholder1']
API_VERSION = '2.12'

SIZE_WARNING_THRESHOLD = 80
SIZE_ERROR_THRESHOLD = 90

def _url(path):
    return f'https://{HOST}' + path

def login(session):
    return session.post(f'https://{HOST}/api/login', headers=apikey, verify=False)

def get_hardware(session):
    session.headers.update(x_auth_token)
    response = session.get(f'https://{HOST}/api/{API_VERSION}/hardware', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Pure FlashBlade hardware")
    #Component status. For api 2.12, valid values are critical, healthy, identifying, unhealthy, unknown, and unused.
    for key in results:
        if key == 'items':
            for items in results[key]:
                if items['status'] == 'healthy' and ('PWR' in items['name'] or 'FB' in items['name']) and 'BAY' not in items['name']:
                    output.add_channel(name=items['name'], value=0, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
                elif items['status'] != 'healthy' and ('PWR' in items['name'] or 'FB' in items['name']) and 'BAY' not in items['name']:
                    output.add_channel(name=items['name'], value=10, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
    print(output.json_result) 

def get_hardware_fan(session):
    session.headers.update(x_auth_token)
    response = session.get(f'https://{HOST}/api/{API_VERSION}/hardware', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Pure FlashBlade hardware - Fan")
    #Component status. For api 2.12, valid values are critical, healthy, identifying, unhealthy, unknown, and unused.
    for key in results:
        if key == 'items':
            for items in results[key]:
                if items['status'] == 'healthy' and 'FAN' in items['name']:
                    output.add_channel(name=items['name'], value=0, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
                elif items['status'] != 'healthy' and 'FAN' in items['name']:
                    output.add_channel(name=items['name'], value=10, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
    print(output.json_result)   

def get_drives(session):
    session.headers.update(x_auth_token)
    response = session.get(f'https://{HOST}/api/{API_VERSION}/drives', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Disks status - Chassis 1")
#Current status of the drive. For api 2.12, valid values are evacuated, evacuating, healthy, unhealthy, unused, and updating.
    count = 1
    for key in results:
        if key == 'items':
            for items in results[key]:
                if items['name'].startswith("CH1"):
                    if items['status'] == 'healthy':
                        output.add_channel(name=items['name'], value=0, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'empty':
                        output.add_channel(name=items['name'], value=1, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'updating':
                        output.add_channel(name=items['name'], value=2, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'unused':
                        output.add_channel(name=items['name'], value=3, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'evacuating':
                        output.add_channel(name=items['name'], value=4, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'identifying':
                        output.add_channel(name=items['name'], value=5, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'unhealthy':
                        output.add_channel(name=items['name'], value=6, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'recovering':
                        output.add_channel(name=items['name'], value=7, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'unrecognized':
                        output.add_channel(name=items['name'], value=8, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'failed':
                        output.add_channel(name=items['name'], value=9, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    if count == 49:
                        break
                    count = count + 1
    print(output.json_result)

# separate chassis to bypass 50 channel limit
def get_drives_2(session):
    session.headers.update(x_auth_token)
    response = session.get(f'https://{HOST}/api/{API_VERSION}/drives', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Disks status - Chassis 2")
#Current status of the drive. For api 2.12, valid values are evacuated, evacuating, healthy, unhealthy, unused, and updating.
    count = 1
    for key in results:
        if key == 'items':
            for items in results[key]:
                if items['name'].startswith("CH2"):
                    if items['status'] == 'healthy':
                        output.add_channel(name=items['name'], value=0, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'empty':
                        output.add_channel(name=items['name'], value=1, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'updating':
                        output.add_channel(name=items['name'], value=2, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'unused':
                        output.add_channel(name=items['name'], value=3, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'evacuating':
                        output.add_channel(name=items['name'], value=4, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'identifying':
                        output.add_channel(name=items['name'], value=5, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'unhealthy':
                        output.add_channel(name=items['name'], value=6, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'recovering':
                        output.add_channel(name=items['name'], value=7, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'unrecognized':
                        output.add_channel(name=items['name'], value=8, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    elif items['status'] == 'failed':
                        output.add_channel(name=items['name'], value=9, value_lookup="prtg.standardlookups.purestorage.drivestatus")
                    if count == 49:
                        break
                    count = count + 1
    print(output.json_result)
    
def get_performance(session):
    session.headers.update(x_auth_token)
    response = session.get(f'https://{HOST}/api/{API_VERSION}/arrays/performance', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("PURE FlashBlade performance")
    for key in results:
        if key == 'items':
            for items in results[key]:
                output.add_channel(name="Write bytes per second", unit="BytesBandwidth", volume_size="KiloByte", value=items['write_bytes_per_sec'])
                output.add_channel(name="Read bytes per second", unit="BytesBandwidth", volume_size="KiloByte", value=items['read_bytes_per_sec'])
                output.add_channel(name="Write IOPS per second", unit="IOPS", value=items['writes_per_sec'])
                output.add_channel(name="Read IOPS per second", unit="IOPS", value=items['reads_per_sec'])
                output.add_channel(name="Write latency", unit="usec", value=items['usec_per_write_op'])
                output.add_channel(name="Read latency", unit="usec", value=items['usec_per_read_op'])
    print(output.json_result)

def get_capacity(session):
    session.headers.update(x_auth_token)
    response = session.get(f'https://{HOST}/api/{API_VERSION}/arrays/space', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("PURE FlashBlade capacity")
    for key in results:
        if key == 'items':
            for items in results[key]:
                output.add_primary_channel(name="Used %", unit=ValueUnit.PERCENT, value=(round(items['space']['total_physical'] * 100 / items['capacity'])), is_limit_mode=True, limit_max_warning=SIZE_WARNING_THRESHOLD, limit_warning_msg="High array disk space usage", limit_max_error=SIZE_ERROR_THRESHOLD, limit_error_msg="Very high array disk space usage")
                #output.add_channel(name="Capacity", unit="PB", value=(items['capacity'] / 1125899906842624))
                output.add_channel(name="Capacity", unit="BytesDisk", volume_size="TeraByte", value=items['capacity'])
                output.add_channel(name="Used space", unit="BytesDisk", volume_size="TeraByte", value=items['space']['total_physical'])
                output.add_channel(name="Available", unit="BytesDisk", volume_size="TeraByte", value=(items['capacity'] - items['space']['total_physical']))
                output.add_channel(name="Snapshot", unit="GB", value=(items['space']['snapshots'] / 1073741824))
                #output.add_channel(name="Snapshot", unit="BytesDisk", volume_size="GigaByte", value=items['space']['snapshots'])
                output.add_channel(name="Free Space %", unit=ValueUnit.PERCENT, value=(round(((items['capacity'] - items['space']['total_physical']) / items['capacity'] * 100))))
                output.add_channel(name="Data reduction", is_float=True, unit=" ", value=(float("{:.2f}".format(items['space']['data_reduction']))))
    print(output.json_result)




#INITIALISATION AND LOGIN
apikey = {"api-token":API_TOKEN}
s = requests.session()
requests.packages.urllib3.disable_warnings()
response = login(s)
if response.status_code == 200:
    x_auth_token = {"x-auth-token":response.headers["X-Auth-Token"]}
else:
    # This means something went wrong.
    print(f"Error {response.status_code}" )


if (perams['scope']) == "hardware":
    get_hardware(s)
elif (perams['scope']) == "hardware_fan":
    get_hardware_fan(s)
elif (perams['scope']) == "drive":
    get_drives(s)
elif (perams['scope']) == "drive_2":
    get_drives_2(s)
elif (perams['scope']) == "performance":
    get_performance(s)
elif (perams['scope']) == "capacity":
    get_capacity(s)
else:
   get_capacity(s)