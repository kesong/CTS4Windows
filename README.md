CTS4Windows
============================
Runnning CTS 7.0 on Windows

Offical CTS could only running on Ubuntu or other Linux Distributions, check the script in the offcial package the CTS console is launched with jar. So I do some adaption to make the scripts could running on windows.<br>
<br>
The script is written in python, and it's very convenient to be modified.<br>

# Precondition
There are some sofeware need to be installed and environment need configured <br>
**python 2.7**<br>
**java 1.8**<br>
**aapt**<br>
**adb**<br>

# Usage:
* Download Compatibility Test Suite from official website, Unzip package on local PC;<br>
'(https://source.android.com/compatibility/cts/downloads)'<br>
for example:<br>
* Step1: android-cts-7.0_r11-linux_x86-arm.zip, unzip it to directory( D:\temp\android-cts-7.0_r11-linux_x86-arm);<br>
* Step2: Do not do any change of the directory, doesn't need change name of directory, just keep it as original format;<br>
* Step3: Copy the script into subdirectory named tools, in this exapmle is "D:\temp\android-cts-7.0_r11-linux_x86-arm\android-cts\tools"<br>
* Step4: open windows commmand line console(cmd), change current directory to the dir as step3, input command: <br>
python cts-tradefed.py<br>

# Notes:
This script developed via android 7.0 CTS, if you want to do android 6.0 or 8.0 CTS test, this script must modify to fit for other platform. <br>
File named 'tradefed.log' will be created in the directory same with the script located, we can check if there is somthing warong when we encounter error during the script running.
