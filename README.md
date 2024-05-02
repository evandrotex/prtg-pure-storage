# prtg-pure-storage
PRTG script to check PURE storage SAN statistics using REST API


![All available sensors](https://github.com/evandrotex/prtg-pure-storage/raw/master/all%20sensors.png)


To use: 
1. Copy necessary files (prtg.standardlookups.purestorage.hardwarestatus.ovl and prtg.standardlookups.purestorage.drivestatus.ovl) to the lookups directory of prtg (C:\Program Files (x86)\PRTG Network Monitor\lookups\custom) and (prtg-pure-storage.py to C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python).
2. Ensure you at least modify the API_TOKEN variable at the top. You can use the pureuser API key for this purpose. For pure-api-v22.py and prtg-pure-flashblade.py set api key as placeholder1, on "Credentials for Script Sensors" under the device settings.
![Api](https://github.com/evandrotex/prtg-pure-storage/raw/master/api-key.png)
3. Modify the url address (prtg-puer-storage.py and pure-api-v20.py). For pure-api-v22.py and prtg-pure-flashblade.py use additional parameter arrayaddress=%host
![Host](https://github.com/evandrotex/prtg-pure-storage/raw/master/additional-parameter.png)
4. Restart PRTG core service to load these files as per https://www.paessler.com/manuals/prtg/prtg_probe_administrator
5. Create a "Python Script Advanced" sensor in PRTG
6. Select the right python script, and add the right additional parameter as the table below. For pure-api-v22.py and prtg-pure-flashblade.py use key=value format (scope=capacity)
![Adding a sensor](https://github.com/evandrotex/prtg-pure-storage/raw/master/add-sensor.png)

7. Create a separate sensor for each switch/parameter


## LIST of SENSOR PARAMETERS
<table>
    <tr>
        <th>switch</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>-v</td>
        <td>List all PURE storage volumes and its front end disk usage (as seen by client) </td>
    </tr>
    <tr>
        <td>-u</td>
        <td>List all PURE storage volumes and its back end disk usage(after dedup/compress with parity overhead)</td>
    </tr>
    <tr>
        <td>-m</td>
        <td>List all manually created volume snapshots and its backend size </td>
    </tr>
    <tr>
        <td>-c</td>
        <td>List PURE storage controllers and their health</td>
    </tr>
    <tr>
        <td>-d</td>
        <td>List PURE storage drives and their health</td>
    </tr>
    <tr>
        <td>-h</td>
        <td>List PURE storage hardware (fans, PSU, chassis, etc) and their health</td>
    </tr>
    <tr>
        <td>-p</td>
        <td>List PURE storage array performance including queue depth (with threshold for warning), IOPS, and RW rate and latency </td>
    </tr>
     <tr>
        <td>-s</td>
        <td>List PURE storage array capacity including snapshot size, data reduction and user definable WARNING and ERROR threshold for disk usage</td>
    </tr>
     <tr>
        <td>-r</td>
        <td>List PURE storage volumes read and write stats in bytes/s</td>
    </tr>
    <tr>
        <td>-i</td>
        <td>List PURE storage volumes IOPS stats</td>
    </tr>
</table>



v20 addition.
Prtg has released its v20 of its prtg network monitor software.
Please use the corresponding script for this version.
Switches are also different and has checks to ensure that channel name is longer than prtg maximum (32 characters) and channel count is less than max (50). If you have more than 50 volumes, this will only display the first 50 returned by the pure storage SAN

## LIST of SENSOR PARAMETERS v20
<table>
    <tr>
        <th>switch</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>-v</td>
        <td>List all PURE storage volumes and its front end disk usage (as seen by client) </td>
    </tr>
    <tr>
        <td>-u</td>
        <td>List all PURE storage volumes and its back end disk usage(after dedup/compress with parity overhead)</td>
    </tr>
    <tr>
        <td>-m</td>
        <td>List all manually created volume snapshots and its backend size </td>
    </tr>
    <tr>
        <td>-c</td>
        <td>List PURE storage controllers and their health</td>
    </tr>
    <tr>
        <td>-d</td>
        <td>List PURE storage drives and their health</td>
    </tr>
    <tr>
        <td>-h</td>
        <td>List PURE storage hardware (fans, PSU, chassis, etc) and their health</td>
    </tr>
    <tr>
        <td>-p</td>
        <td>List PURE storage array performance including queue depth (with threshold for warning), IOPS, and RW rate and latency </td>
    </tr>
     <tr>
        <td>-s</td>
        <td>List PURE storage array capacity including snapshot size, data reduction and user definable WARNING and ERROR threshold for disk usage</td>
    </tr>
     <tr>
        <td>-br</td>
        <td>List PURE storage volumes read stats in bytes/s</td>
    </tr>
    <tr>
        <td>-bw</td>
        <td>List PURE storage volumes write stats in bytes/s</td>
    </tr>
    <tr>
        <td>-ir</td>
        <td>List PURE storage volumes read IOPS stats</td>
    </tr>
        <tr>
        <td>-iw</td>
        <td>List PURE storage volumes write IOPS stats</td>
    </tr>
    </tr>
        <tr>
        <td>-q</td>
        <td>List PURE storage volumes queue depth</td>
    </tr>

</table>

v22 addition.
Prtg has released its v22 of its prtg network monitor software.
Please use the corresponding script for this version. Example for additional paramenter scope=hardware

## LIST of SENSOR PARAMETERS v22
<table>
    <tr>
        <th>scope</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>volumes</td>
        <td>List all PURE storage volumes and its front end disk usage (as seen by client) </td>
    </tr>
    <tr>
        <td>usage</td>
        <td>List all PURE storage volumes and its back end disk usage(after dedup/compress with parity overhead)</td>
    </tr>
    <tr>
        <td>snapshots</td>
        <td>List all manually created volume snapshots and its backend size </td>
    </tr>
    <tr>
        <td>controllers</td>
        <td>List PURE storage controllers and their health</td>
    </tr>
    <tr>
        <td>drive</td>
        <td>List PURE storage drives and their health</td>
    </tr>
    <tr>
        <tr>
        <td>shelf</td>
        <td>List PURE storage shelf drives and their health</td>
    </tr>
    <tr>
        <td>hardware</td>
        <td>List PURE storage hardware (fans, PSU, chassis, etc) and their health</td>
    </tr>
    <tr>
        <td>performance</td>
        <td>List PURE storage array performance including IOPS and RW rate and latency </td>
    </tr>
     <tr>
        <td>capacity</td>
        <td>List PURE storage array capacity including snapshot size, data reduction and user definable WARNING and ERROR threshold for disk usage</td>
    </tr>
     <tr>
        <td>bytesread</td>
        <td>List PURE storage volumes read stats in bytes/s</td>
    </tr>
    <tr>
        <td>byteswrite</td>
        <td>List PURE storage volumes write stats in bytes/s</td>
    </tr>
    <tr>
        <td>ioread</td>
        <td>List PURE storage volumes read IOPS stats</td>
    </tr>
        <tr>
        <td>iowrite</td>
        <td>List PURE storage volumes write IOPS stats</td>
    </tr>
</table>

Flashblade options.
Please use the corresponding script for this version. Example for additional paramenter scope=hardware

## LIST of SENSOR PARAMETERS Flashblade
<table>
    <tr>
        <th>scope</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>hardware</td>
        <td>List PURE storage Flashblade hardware (PSU, chassis, etc) and their health</td>
    </tr>
        <tr>
        <td>hardware_fan</td>
        <td>List PURE storage Flashblade hardware fans and their health</td>
    </tr>
     <tr>
        <tr>
        <td>drive</td>
        <td>List PURE storage Flashblade drives and their health</td>
    </tr>
    <tr>
        <tr>
        <td>drive_2</td>
        <td>List PURE storage Flashblade drives from second controller and their health</td>
    </tr>
    <tr>
        <td>performance</td>
        <td>List PURE storage Flashblade performance including IOPS and RW rate and latency </td>
    </tr>
     <tr>
        <td>capacity</td>
        <td>List PURE storage Flashblade capacity including snapshot size, data reduction and user definable WARNING and ERROR threshold for disk usage</td>
    </tr>
</table>

## Troubleshooting

In case of error, set the debug mode on 
https://kb.paessler.com/en/topic/59621-how-can-i-activate-log-writting

If you need to install python modules, follow these guide

https://kb.paessler.com/en/topic/90686-i-want-to-install-python-packages-for-the-python-installation-of-prtg-how-can-i-do-that


![All available sensors](https://github.com/evandrotex/prtg-pure-storage/raw/master/install_requests.png)

