# /usr/bin/env python 

"""
	Author: song.ke
	This script is for running CTS on windows.(Have test on windows 7)
	Before run the script, there are something of environment should be configured
	aap, adb, java should installed first
	Unzip official CTS package and put the script in the path\\to\\android-cts\\tools directory 
	Open the terminal of windows and run command as following:
	>python cts-tradefed.py
"""

import os
import subprocess
import fnmatch
import re
import time
import sys

"""
#JAR_PATH: "All of testcases and cts console."
#JAR_DIR: "For test jars, jars to run cts consle"
#CTS_ROOT: "xxx\\android-cts\\tools"
#TFDEBUG: ""
#TF_DEBUG_PORT: "
"""

global JAR_DIR
global JAR_PATH
global CTS_ROOT
global TFDEBUG
global TF_DEBUG_PORT
global SCRIPT_PATH

JAR_PATH = ''
SCRIPT_PATH = None

def checkFile(filename):
	if os.path.isfile(filename):
		log(filename + " located.")
		return True
	else:
		log("Unable to locate " + filename)
		return False

def runCommand(cmd):
	cmdOutput = []
	output_dest = subprocess.PIPE
	input_dest = subprocess.PIPE
	pipe = subprocess.Popen(cmd, stdin=None, stdout=output_dest, stderr=subprocess.STDOUT, shell=True)
	try:
		outputs = pipe.communicate()[0]
		if outputs is not None and len(outputs) > 0:
			cmdOutput.append(outputs)
	except OSError, e:
		print "Command not found!"
	log(cmdOutput)
	return cmdOutput

def cmdResultCheck(resultList, srcString):
	firstString = "".join(resultList).split('\r\n')[0]
	secondString = re.match('^[a-zA-Z" "]*[a-zA-Z$]', firstString).group(0)
	if cmp(srcString, secondString) == 0:
		log(srcString + ' found.')
		return True
	else:
		log("The " + secondString + " is not found")
		return False

def checkCommand(cmd, cmd_str):
	cmd_exist = False
	cmd_exist = cmdResultCheck(runCommand(cmd), cmd_str)
	if cmd_exist:
		return True
	else:
		return False

# check aapt
def checkAAPT():
	aapt_cmd = "aapt version"
	aapt_str = "Android Asset Packaging Tool"
	if checkCommand(aapt_cmd, aapt_str):
		print aapt_cmd + ' found.'
	else:
		print aapt_cmd + ' not found. You should configure aapt first.'

# check adb
def checkADB():
	adb_cmd = "adb version"
	adb_str = "Android Debug Bridge version"
	if checkCommand(adb_cmd, adb_str):
		print adb_cmd + ' found.'
	else:
		print adb_cmd + ' not found. You should configure adb first.'

# check Java and version(1.6, 1.7 or 1.8 required)
def checkJava():
	java_cmd = "java -version"
	java_str = "java version"
	jv = ""
	verNo = 0
	jv = "".join(runCommand(java_cmd)).split('\r\n')[0]
	log(jv)
	verNo = re.search('[ ""]1\.[678][\. "$$"]', jv).group(0)
	log(verNo)
	if verNo is not None:
		print "java found, version is greater than or equal to 1.6."
		return True
	else:
		print  "java not found, and version 1.6, 1.7 or 1.8 is required."
		return False

def checkEnv(env_str):
	if os.getenv(env_str) is not None:
		return True
	else:
		return False

# check debug flag and set up remote debugging
def checkTFdebug():
	if checkEnv('TFDEBUG'):
		if os.getenv('TF_DEBUG_PORT') is None:
			TF_DEBUG_PORT = 10088
	RDBG_FLAG = "-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=" + TF_DEBUG_PORT

"""
# check if in Android build env
def checkAndroidEnv():
	if checkEnv('ANDROID_BUILD_TOP') and checkEnv('ANDROID_HOST_OUT'):
		CTS_ROOT = os.getenv('ANDROID_HOST_OUT') + '\\cts'
	else:
		CTS_ROOT = os.getenv('ANDROID_BUILD_TOP') + '\\' + os.getenv('OUT_DIR:-out') + '\\host' + '\\' + os.getenv('OS') + '\\cts'
"""
# define the CTS root directory, make sure running cts-tradefed.py in the "anypath\android-cts\tools" directory.
def defCTSroot():
	CTS_ROOT = None
	if not checkEnv('CTS_ROOT'):
		#CTS_ROOT_PATH =  os.path.abspath(os.getcwd() + "\\..\\..")
		CTS_ROOT_PATH =  SCRIPT_PATH + "\\..\\.."
		log(CTS_ROOT_PATH)
		os.environ['CTS_ROOT'] = CTS_ROOT_PATH
		if checkEnv('CTS_ROOT'):
			log(os.getenv('CTS_ROOT'))

def addJars(jars):
	global JAR_PATH
	JAR_DIR = os.getenv('CTS_ROOT') + "\\android-cts\\tools"
	for jarItem in jars:
		jarName = os.path.abspath(JAR_DIR) + '\\' + jarItem + '.jar'
		if checkFile(jarName):
			JAR_PATH += jarName + ';'
	log(JAR_PATH)

def addDefaultJars():
	JARS = ['tradefed-prebuilt', 'hosttestlib', 'compatibility-host-util', 'cts-tradefed']
	addJars(JARS)

def addOptionalJars():
	OPTIONAL_JARS = ['google-tradefed', 'google-tradefed-tests', 'google-tf-prod-tests']
	addJars(OPTIONAL_JARS)

def addtestJars():
	global JAR_PATH
	CASE_PATH = os.getenv('CTS_ROOT') + '\\android-cts\\testcases'
	log(CASE_PATH)
	log(os.listdir(CASE_PATH))
	for caseJars in os.listdir(CASE_PATH):
		if re.search('\.jar$', caseJars) is not None:
			JAR_PATH += os.path.abspath(CASE_PATH) + '\\' + caseJars + ';'
	log(JAR_PATH) 

def log(msg):
	global SCRIPT_PATH
	SCRIPT_PATH = os.path.split(os.path.realpath(sys.argv[0]))[0]
	logPath = SCRIPT_PATH + '\\tradefed.log'
	logtime = time.strftime('%d/%m/%Y-%H:%M:%S')
	logString = '-->%s - %s' % (logtime, msg)
	logFile = file(logPath, 'a+')
	logFile.write('\n' + logString)
	logFile.close()

def main():
	startTime = time.strftime('%d/%m/%Y-%H:%M:%S')
	delimiterStr = "<=========================Testing Start at " + startTime + "=========================>"
	log(delimiterStr)

	log("Check if aapt is configured.")
	checkAAPT()

	log("Check if java could running and the version is 1.6, 1.7 or 1.8.")
	checkJava()

	log("Check if adb is configured.")
	checkADB()

	log('Define CTS_ROOT.')
	defCTSroot()

	log("Add cts default .jar in android-cts\\tools to JAR_PATH")
	addDefaultJars()

	log("Add optional .jar into JAR_PATH, theses jars are google provide.")
	addOptionalJars()

	log("Add jars of testcases into JAR_PATH, in android-cts\\testcases directory.")
	addtestJars()

	ctsConsole = 'com.android.compatibility.common.tradefed.command.CompatibilityConsole'
	DCTS_ROOT = '-DCTS_ROOT=' + os.getenv('CTS_ROOT')
	CTS_TRADEFED = 'java -cp ' + JAR_PATH
	CTS_TRADEFED += ' ' + DCTS_ROOT
	CTS_TRADEFED += ' ' + ctsConsole
	log(CTS_TRADEFED)
	log("Launch CTS Console, cts will start once the console launch successfully.")
	os.system(CTS_TRADEFED)

if __name__ == '__main__':
	main()