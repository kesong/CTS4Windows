CTS4Windows
============================
Runnning CTS 7.0 on Windows

Offical CTS could only running on Ubuntu or other Linux Distributions, check the script in the offcial package the CTS console is launched with jar. So I do some adaption to make the scripts could running on windows.

The script is written in python, and it's very convenient to be modified.

# Precondition
.python 2.7<br>
.java 1.8<br>
.aapt<br>
.adb<br>

# Usage:
1. Download Compatibility Test Suite from official website, Unzip package on local PC;
https://source.android.com/compatibility/cts/downloads
for example:
(1)android-cts-7.0_r11-linux_x86-arm.zip, unzip it to directory( D:\temp\android-cts-7.0_r11-linux_x86-arm)
(2)Do not do any change of the directory, doesn't need change name of directory, just keep it as original format;
(3)Copy the script into subdirectory named tools, in this exapmle is "D:\temp\android-cts-7.0_r11-linux_x86-arm\android-cts\tools"
(4)open windows commmand line console(cmd), change current directory to the dir as step3, input command: python cts-tradefed.py


# Notes:
This script developed via android 7.0 CTS, if you want to do android 6.0 or 8.0 CTS test, this script must modify to fit for other platform.
