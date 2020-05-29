#REQUIREMENTS
#One should have gitpython module installed for this code to run if not present use this command to get it "pip install GitPython"
#This code only supports python version >= 3.4

import os
import subprocess
import git
import time
import sys

src_ssh = "ssh://wmgit.pramati.com:29418/"
sudoPassword = ""

#running mvn build command
def run(dir):
    os.chdir(dir)
    process = subprocess.Popen(
        "mvn clean install -DskipTests=true",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    log(out, dir)
    errcode = process.returncode
    return (out, err, errcode)

#running ant build command
def runfrontend(dir):
    os.chdir(dir)
    myCmd = subprocess.Popen(
        "ant build-full-local",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = myCmd.communicate()
    logfront(out, dir)
    errcode = myCmd.returncode
    return (out,err, errcode)

#log verification for mvn build command
def log(out, dir):
    if "[INFO] BUILD SUCCESS\n[INFO]" in str(out, "UTF-8"):
        print("SUCCESS for %s " % dir)
    else:
        with open("log.log", "wb") as f:
            f.write(out)
        print("FAILED for %s see %s" % (dir, dir + "/log.log"))

#log verification for ant build command
def logfront(out, dir):
    if "BUILD SUCCESS" in str(out, "UTF-8"):
        print("SUCCESS for %s " % dir)
    else:
        with open("log.log", "wb") as f:
            f.write(out)
        print("FAILED for %s see %s" % (dir, dir + "/log.log"))

#building images by using docker-compose-build.sh
def buildimages(dir):
    os.chdir(dir)
    os.system("echo 'export WAVEMAKER_STUDIO_SERVICES_CODEBASE=~/build/localimages/wavemaker-studio-services/' | cat - docker-compose-build.sh > temp && mv temp docker-compose-build.sh")
    os.system("echo 'export WAVEMAKER_STUDIO_FRONTEND_CODEBASE=~/build/localimages/wavemaker-studio-frontend/' | cat - docker-compose-build.sh > temp && mv temp docker-compose-build.sh")
    command = 'bash docker-compose-build.sh'
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

#clone at root position 
def gitclone_r(module):
    git.Git(root).clone(src_ssh + module)

#clone at backend module
def gitclone_b(module):
    git.Git(root + "wavemaker-studio-services").clone(src_ssh + module)

#clone at frontend module
def gitclone_f(module):
    git.Git(root + "wavemaker-studio-frontend").clone(src_ssh + module)

#pusing docker images created
def pushimages():
    command="docker push 192.168.2.44:5000/dev/tomcat-base:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/studio-mysql:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/studio-tomcat:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/studio-apps-tomcat:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/studio-nginx:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/embedded-codebase-studio-tomcat:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/embedded-codebase-studio-apps-tomcat:latest:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    command="docker push 192.168.2.44:5000/dev/embedded-codebase-studio-nginx:latest"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))


if __name__ == "__main__":
    start_time = time.time()
    os.system("mkdir -p ~/localimages")
    root = os.getcwd()+"/localimages/"
    os.system("rm -rf " + root)
    os.system("mkdir " + root)

    git.Git(root).clone("master:"+src_ssh + "wmo-ops")


    end_time = time.time()
    mins, secs = divmod(end_time-start_time, 60)
    print("Total running time %d min:%d sec.\n" % (mins, secs))
