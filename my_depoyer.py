#!/usr/bin/env python3
import os
import subprocess
import argparse


def main():
    """main function"""
    #Docker Version Verification
    if os.system('docker -v') == 0:
        getVersion = subprocess.check_output("docker -v"
        ).decode("utf-8").split()
        dockerVersion = float(getVersion[2][:5])
        if dockerVersion < 19.03:
            print("Older version of docker detected, updating ...")
            os.system('apt-get update docker')
        else:
            print("Docker is installed and up to date.")
    else:
        print("Docker is not installed. Downloading docker...")
        os.system('apt-get install docker:latest')

    #Création de la commande build
    parser = argparse.ArgumentParser(description =
        'Build single or multiple microservices.')
    parser.add_argument('-v', action='store_true', help='v help')
    subparser = parser.add_subparsers(help="Subcommand help")
    build_command=subparser.add_parser('build', help='Build microservices')
    build_command.add_argument('value',
        choices = ['checker', 'micros2','all'],
        type = str, nargs = '+',
        help = 'one or more microservices from : checker, micros2')
    args = parser.parse_args()
    arg_list=args.value
    
    all_bool = False #Boolean permettant tous, un, ou plusieurs builds
    
    #Vérification de la présence de l'argument all
    for arg in arg_list:
        if arg == "all":
            os.chdir('./checker')
            os.system('docker build -t checker:1.0 .')
            #os.system('docker build -t micros:1.0 .')
            os.system('docker run -it -v /var/run/docker.sock:/var/run/docker.sock -p 7000:5000 checker:1.0')
            #os.system('docker run -it -d -v /var/run/docker.sock:/var/run/docker.sock -p 8000:6000 micros2:1.0')')
            os.chdir('..')
            all_bool = True
    
    #Vérification que la commande all n'est pas présente
    if all_bool != True:
        for arg in arg_list:
            if arg == "checker":
                os.chdir('./checker')
                os.system('docker build -t checker:1.0 .') 
                os.system('docker run -it -v /var/run/docker.sock:/var/run/docker.sock -p 7000:5000 checker:1.0')
                os.chdir('..')
            if arg == "micros2":
                os.chdir('./checker')
                #os.system('docker build -t micros:1.0 .') 
                #os.system('docker run -it -d -v /var/run/docker.sock:/var/run/docker.sock -p 8000:6000 micros2:1.0')')
                os.chdir('..')


if __name__ == "__main__":
    main()
