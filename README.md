# GPredict_DISH_Tailgater_Rotator_Interface

after 6 hours of looking around at other existing repos and writing sloppy code i present to you the "GPredict_DISH_Tailgater_Rotator_Interface" or GDTRI for short.

### Description:
GDTRI is a simple and sloppy python script to interface GPredict with a DISH Tailgater device.
This script currently works and has been tested on a DISH Tailgater 3 under linux and under windows 11. 
This project was inspired by https://github.com/saveitforparts/Tailgater-Microwave-Imaging and uses some of the code from that repo.
If anybody wants to clean up my code feel free to do so and tell me about it at aanzell00@gmail.com and also feel free to tell me about how it works with other DISH Tailgater versions if you have one of a different model than mine.

### Important notes:
The DISH Tailgater requires around 13V through Coax to function properly.
under Linux the device may sometimes be connected as /dev/ttyACM1 or /dev/ttyACM2 instead of /dev/ttyACM0. To fix this all you need to do is change the port to the correct serial port.
Under Windows, you will need to change the Serial port in the code to the correct COM port in device manager for this script to function.
in GPredict when you add a rotator the minimum Elevation WILL need to be adjusted to avoid excess wear on your DISH Tailgater (mine only goes down to about 7 degrees before it starts hitting the bottom of the frame)

