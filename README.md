# rpcs_activity_sensing
Code for CMU 18745 - Rapid Prototyping of Computer Systems Activity Sensing team

This code enables you to program the UHF RFID readers. You must be conected through RS232-USB cable.

### rfid_config.py
This runs on the Raspberry Pi and is used to configure the RFID reader before operation.

### rfid_stream.py
A continuous while loop that continuously lists wristbands that are being read by the reader.

### masterPi.py
Script to run on the master node to read in data copied from the slaves, do filtering for conflict detection, then send to the backend's server

### slave_setup.txt
Instructions on setting up a slave node

### master_setup.txt
Instructions on setting up a master node


#### Notes
It would be really nice to have everything be docker containers, then use
docker environment variables to set variables between slaves and the master.
We don't have tons of time for that, but it'd be nice - we'd have a
guarentuee of consistency that things like IP addresses and formats
are consistent that's more than just "Is everything synced with Github".

Currently, the system only allows one reader per Pi, but this could be changed.
Ideally, four readers could be attached to a slave, but this might not work -
USB-RS232 cables have a max length.

Additionally it would be nice to have the backend server act as the master node
 - it would be much more efficient to have the filtering computation be done
on a more powerful computer. We didn't plan for this when we decided on
interfaces and there was never a good time to try to do the interface switch.
It's also out of scope to have the backend do those sorts of calculations,
but the activity sensing team could have written the code to run on the backend
server.



## System Setup
The system runs two Chafon 6M RFID readers connected over USB<->RS232 cables.
The Pis run stock Raspbian flashed onto an SD card, with no modifications
(save for installing vim/zsh for a more reasonable dev environment).
All our code is in Python scripts, we used Python 2.7.6

To run the system, one needs to ensure that all slaves are synced to the github
repo (i.e. will send data to the master at around the same time, the master IP
is the same on all nodes).

On each slave, run `python rfid_stream.py`. This sends data to the master at
9PM every day.

On the master, a cron job needs to be setup to run `python masterPi.py` at midnight
every day.

For debugging, it's helpful to remove the `os.remove` calls in `masterPi.py` so that intermediate output can be seen.
