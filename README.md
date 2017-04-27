# rpcs_activity_sensing
Code for CMU 18745 - Rapid Prototyping of Computer Systems Activity Sensing team

This code enables you to program the UHF RFID readers. You must be conected through RS232-USB cable. 

### rfid_config.py
This runs on the Raspberry Pi and is used to configure the RFID reader before operation.

### rfid_stream.py
A continuous while loop that continuously lists wristbands that are being read by the reader.

### masterPi.py
Script to run on the master node to read in data copied from the slaves, do filtering for conflict detection, then send to the backend's server



#### Notes
It would be really nice to have everything be docker containers, then use docker environment variables to set variables between slaves and the master. We don't have tons of time for that, but it'd be nice.
