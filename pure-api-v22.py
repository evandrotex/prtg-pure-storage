# -*- coding: utf-8 -*-
#!/usr/bin/python

# Usage
# Setup api key as "Credentials for Script Sensors" placeholder 1 (if other position is used, change line 27).
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
API_VERSION = '1.15'

SIZE_WARNING_THRESHOLD = 80
SIZE_ERROR_THRESHOLD = 90

def _url(path):
    return f'https://{HOST}' + path

def login(session):
    return session.post(f'https://{HOST}/api/{API_VERSION}/auth/session', json=apikey, verify=False)

def get_volumes(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("Provisioned size")
    count = 1
    for item in results:
        channel_name = item['name']
        if len(channel_name) > 32:
          channel_name = channel_name[0:31]
        output.add_channel(name=channel_name, unit="BytesDisk", volume_size="TeraByte", value=item['size'])
        if count == 50:
            break
        count = count + 1
    print(output.json_result)

def get_volumes_usage(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("Array real usage per volume")
    count = 1
    for item in results:
        channel_name = item['name']
        if len(channel_name) > 32:
          channel_name = channel_name[0:31]
        output.add_channel(name=channel_name, unit="Bytes", value=item['total'])
        if count == 50:
            break
        count = count + 1
    print(output.json_result)

def get_volumes_io_r(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("Volumes IO read performance")
    count = 1
    for item in results:
        query = f'https://{HOST}/api/{API_VERSION}/volume' + '/' + item['name'] + '?action=monitor'
        new_response = session.get(query, verify=False)
        new_results = json.loads(new_response.text)
        channel_name = item['name']
        if len(channel_name) > 30:
          channel_name = channel_name[0:29]
        output.add_channel(name=channel_name +' R', unit="IOPS", value=new_results[0]['reads_per_sec'])
        if count == 50:
            break
        count = count + 1
    print(output.json_result)

def get_volumes_io_w(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("Volumes IO write performance")
    count = 1
    for item in results:
        query = f'https://{HOST}/api/{API_VERSION}/volume' + '/' + item['name'] + '?action=monitor'
        new_response = session.get(query, verify=False)
        new_results = json.loads(new_response.text)
        channel_name = item['name']
        if len(channel_name) > 30:
          channel_name = channel_name[0:29]
        output.add_channel(name=channel_name +' W', unit="IOPS", value=new_results[0]['writes_per_sec'])
        if count == 50:
            break
        count = count + 1
    print(output.json_result)
 
def get_volumes_bytes_r(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("Volumes bytes Read performance")
    count = 1
    for item in results:
        query = f'https://{HOST}/api/{API_VERSION}/volume' + '/' + item['name'] + '?action=monitor'
        new_response = session.get(query, verify=False)
        new_results = json.loads(new_response.text)
        channel_name = item['name']
        if len(channel_name) > 30:
          channel_name = channel_name[0:29]
        output.add_channel(name=channel_name + ' R', unit="BytesBandwidth", value=new_results[0]['input_per_sec'])
        if count == 50:
            break
        count = count + 1
    print(output.json_result)

def get_volumes_bytes_w(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("Volumes bytes Write performance")
    count = 1
    for item in results:
        query = f'https://{HOST}/api/{API_VERSION}/volume' + '/' + item['name'] + '?action=monitor'
        new_response = session.get(query, verify=False)
        new_results = json.loads(new_response.text)
        channel_name = item['name']
        if len(channel_name) > 30:
          channel_name = channel_name[0:29]
        output.add_channel(name=channel_name + ' W', unit="BytesBandwidth", value=new_results[0]['output_per_sec'])
        if count == 50:
            break
        count = count + 1
    print(output.json_result)

def get_controllers(session):
    output = CustomSensorResult("Pure storage controllers")
    response = session.get(f'https://{HOST}/api/{API_VERSION}/array?controllers=true', verify=False)
    results = json.loads(response.text)
    for item in results:
        if item['status'] == 'ready':
            output.add_channel(name=item['mode'], value=0, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
        else:
            output.add_channel(name=item['mode'], value=10, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
    print(output.json_result)     

def get_hardware(session):
    output = CustomSensorResult("Pure storage hardware")
    response = session.get(f'https://{HOST}/api/{API_VERSION}/hardware', verify=False)
    results = json.loads(response.text)
    for item in results:
        if item['status'] == 'ok' and ('FAN' in item['name'] or 'PWR' in item['name'] or 'FC' in item['name']):
            output.add_channel(name=item['name'], value=0, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
        elif item['status'] != 'ok' and ('FAN' in item['name'] or 'PWR' in item['name'] or 'FC' in item['name']):
            output.add_channel(name=item['name'], value=10, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
    print(output.json_result)     


def get_drives(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/drive', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Disks status")
    count = 1
    for item in results:
        if item['name'].startswith("CH"):
            if item['status'] == 'healthy':
                output.add_channel(name=item['name'], value=0, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'empty':
                output.add_channel(name=item['name'], value=1, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'updating':
                output.add_channel(name=item['name'], value=2, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'unused':
                output.add_channel(name=item['name'], value=3, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'evacuating':
                output.add_channel(name=item['name'], value=4, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'identifying':
                output.add_channel(name=item['name'], value=5, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'unhealthy':
                output.add_channel(name=item['name'], value=6, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'recovering':
                output.add_channel(name=item['name'], value=7, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'unrecognized':
                output.add_channel(name=item['name'], value=8, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'failed':
                output.add_channel(name=item['name'], value=9, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            if count == 49:
                break
            count = count + 1
    
    print(output.json_result)
    
# separate shelf disks to bypass 50 channel limit
def get_shelf_drives(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/drive', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Disks shelf status")
    count = 1
    for item in results:
        if item['name'].startswith("SH"):
            if item['status'] == 'healthy':
                output.add_channel(name=item['name'], value=0, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'empty':
                output.add_channel(name=item['name'], value=1, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'updating':
                output.add_channel(name=item['name'], value=2, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'unused':
                output.add_channel(name=item['name'], value=3, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'evacuating':
                output.add_channel(name=item['name'], value=4, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'identifying':
                output.add_channel(name=item['name'], value=5, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'unhealthy':
                output.add_channel(name=item['name'], value=6, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'recovering':
                output.add_channel(name=item['name'], value=7, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'unrecognized':
                output.add_channel(name=item['name'], value=8, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            elif item['status'] == 'failed':
                output.add_channel(name=item['name'], value=9, value_lookup="prtg.standardlookups.purestorage.drivestatus")
            if count == 49:
                break
            count = count + 1
    
    print(output.json_result)

def get_manual_snapshots(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/volume?snap=true&space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("List of manually created snapshots")
    output.add_channel(name="placeholder", unit="Bytes", value=0)
    count = 1
    for item in results:
        channel_name = item['name']
        if len(channel_name) > 32:
          channel_name = channel_name[0:31]
        if ( "Standard-Snaps" not in item['name'] ):
            output.add_channel(name=channel_name, unit="Bytes", value=item['snapshots'], is_limit_mode=True, limit_max_warning=100000000000, limit_warning_msg="Snapshot size too large")
        if count == 49:
            break
        count = count + 1
    print(output.json_result)

def get_performance(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/array?action=monitor', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("PURE array performance")
    for item in results:
        output.add_channel(name="Write bytes per second", unit="Bytes", value=item['output_per_sec'])
        output.add_channel(name="Read bytes per second", unit="Bytes", value=item['input_per_sec'])
        #output.add_primary_channel(name="Queue depth", value=item['queue_depth'], is_limit_mode=True, limit_max_warning=60, limit_warning_msg="Large queue depth")
        output.add_channel(name="Write IOPS per second", unit="IOPS", value=item['writes_per_sec'])
        output.add_channel(name="Read IOPS per second", unit="IOPS", value=item['reads_per_sec'])
        output.add_channel(name="Write latency", unit="usec", value=item['usec_per_write_op'])
        output.add_channel(name="Read latency", unit="usec", value=item['usec_per_read_op'])
    print(output.json_result)

def get_capacity(session):
    response = session.get(f'https://{HOST}/api/{API_VERSION}/array?space=true', verify=False)
    results = json.loads(response.text)
    # create sensor result
    output = CustomSensorResult("PURE array capacity")
    for item in results:
        output.add_channel(name="Capacity", unit="BytesDisk", volume_size="TeraByte", value=item['capacity'])
        output.add_channel(name="Available", unit="BytesDisk", volume_size="TeraByte", value=(item['capacity'] - item['total']))
        output.add_channel(name="Snapshot", unit="BytesDisk", volume_size="TeraByte", value=item['snapshots'])
        output.add_channel(name="Used space", unit="BytesDisk", volume_size="TeraByte", value=item['total'])
        output.add_primary_channel(name="Used %", unit=ValueUnit.PERCENT, value=(round(item['total'] * 100 / item['capacity'])), is_limit_mode=True, limit_max_warning=SIZE_WARNING_THRESHOLD, limit_warning_msg="High array disk space usage", limit_max_error=SIZE_ERROR_THRESHOLD, limit_error_msg="Very high array disk space usage")
        output.add_channel(name="Free Space %", unit=ValueUnit.PERCENT, value=(round((item['capacity'] - item['total']) / item['capacity'] * 100)))
        output.add_channel(name="Data reduction", is_float=True, unit=" ", value=(float("{:.2f}".format(item['data_reduction']))))
    print(output.json_result)



#INITIALISATION AND LOGIN
apikey = {"api_token": API_TOKEN}
s = requests.session()
requests.packages.urllib3.disable_warnings()
response = login(s)
if response.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    


if (perams['scope']) == "volumes":
    get_volumes(s)
elif (perams['scope']) == "usage":
    get_volumes_usage(s)
elif (perams['scope']) == "snapshots":
    get_manual_snapshots(s)
elif (perams['scope']) == "controllers":
    get_controllers(s)
elif (perams['scope']) == "drive":
    get_drives(s)
elif (perams['scope']) == "shelf":
    get_shelf_drives(s)
elif (perams['scope']) == "hardware":
    get_hardware(s)
elif (perams['scope']) == "performance":
    get_performance(s)
elif (perams['scope']) == "capacity":
    get_capacity(s)
elif (perams['scope']) == "bytesread":
    get_volumes_bytes_r(s)
elif (perams['scope']) == "byteswrite":
    get_volumes_bytes_w(s)
elif (perams['scope']) == "ioread":
    get_volumes_io_r(s)
elif (perams['scope']) == "iowrite":
    get_volumes_io_w(s)
else:
    get_capacity(s)