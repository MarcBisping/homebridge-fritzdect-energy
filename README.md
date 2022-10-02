# homebridge-fritzdect-energy

I installed a small power plant with a maximum power of 600 W (german so-called "Balkonkraftwerk") via a Fritz!DECT 210 power socket.

To display the actual generated power I wrote a small program, which runs periodically on my Raspberry Pi (cronjob).
The program talks to my Fritz!Box directly to get the actual values of temperature and power and saves this values to a textfile on the Raspberry Pi.

In homebridge I use the plugin "Homebridge Temperature Humidity Sensor File" (homebridge-temperature-humidity-sensor-file v1.1.0) to read the textfiles and to display its values as sensor data.

Since there is no energy-sensor I am mis-using the "humidity-sensor" calculating the actual power as a percent of maximum power 600 W - so a value of 50% reads as 300 W.

If you are interested in this solution please let me know.

Cheers, Marc
