from netmiko import ConnectHandler
from log import authLog

import traceback
import re
import os

shHostname = "show run | i hostname"
shVlanID1101 = "show vlan id 1101"
shVlanID1103 = "show vlan id 1103"
snoopTrust = "ip dhcp snooping trust"

intPatt = r'[a-zA-Z]+\d+\/(?:\d+\/)*\d+'

vlan1101IntList = []
vlan1103IntList = []

def dhcpSnooopTr(validIPs, username, netDevice):
    # This function is to take a show run

    for validDeviceIP in validIPs:
        try:
            validDeviceIP = validDeviceIP.strip()
            currentNetDevice = {
                'device_type': 'cisco_xe',
                'ip': validDeviceIP,
                'username': username,
                'password': netDevice['password'],
                'secret': netDevice['secret'],
                'global_delay_factor': 2.0,
                'timeout': 120,
                'session_log': 'netmikoLog.txt',
                'verbose': True,
                'session_log_file_mode': 'append'
            }

            print(f"Connecting to device {validDeviceIP}...")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                try:
                    sshAccess.enable()
                    shHostnameOut = sshAccess.send_command(shHostname)
                    authLog.info(f"User {username} successfully found the hostname {shHostnameOut}")
                    shHostnameOut = shHostnameOut.replace('hostname', '')
                    shHostnameOut = shHostnameOut.strip()
                    shHostnameOut = shHostnameOut + "#"

                    print(f"INFO: Taking a \"{shVlanID1101}\" for device: {validDeviceIP}")
                    shVlanID1101Out = sshAccess.send_command(shVlanID1101)
                    authLog.info(f"Automation successfully ran the command:{shVlanID1101}\n{shHostnameOut}{shVlanID1101}\n{shVlanID1101Out}")
                    shVlanID1101Out1 = re.findall(intPatt, shVlanID1101Out)
                    authLog.info(f"The following interfaces were found under the command: {shVlanID1101}: {shVlanID1101Out1}")

                    if shVlanID1101Out1:
                        for interface in shVlanID1101Out1:
                            interface = interface.strip()
                            print(f"INFO: Checking configuration for interface {interface} on device {validDeviceIP}")
                            authLog.info(f"Checking configuration for interface {interface} on device {validDeviceIP}")
                            interfaceOut = sshAccess.send_command(f'show run int {interface}')
                            if snoopTrust in interfaceOut:
                                print(f"INFO: Interface {interface} has configured {snoopTrust} on device {validDeviceIP}")
                                authLog.info(f"Interface {interface} has configured {snoopTrust} on device {validDeviceIP}")
                                vlan1101IntList.append(f"Interface {interface} has configured {snoopTrust}")
                            else:
                                print(f"INFO: Interface {interface} does NOT have configured {snoopTrust} on device {validDeviceIP}")
                                authLog.info(f"Interface {interface} does NOT have configured {snoopTrust} on device {validDeviceIP}")
                                vlan1101IntList.append(f"Interface {interface} does NOT have configured {snoopTrust}")
                    else:
                        print(f"INFO: No interfaces found under {shVlanID1101}")
                        authLog.info(f"No interfaces found under {shVlanID1101}")

                    print(f"INFO: Taking a \"{shVlanID1103}\" for device: {validDeviceIP}")
                    shVlanID1103Out = sshAccess.send_command(shVlanID1103)
                    authLog.info(f"Automation successfully ran the command:{shVlanID1103}\n{shHostnameOut}{shVlanID1103}\n{shVlanID1103Out}")
                    shVlanID1103Out1 = re.findall(intPatt, shVlanID1103Out)
                    authLog.info(f"The following interfaces were found under the command: {shVlanID1103}: {shVlanID1103Out1}")

                    if shVlanID1103Out1:
                        for interface in shVlanID1103Out1:
                            interface = interface.strip()
                            print(f"INFO: Checking configuration for interface {interface} on device {validDeviceIP}")
                            authLog.info(f"Checking configuration for interface {interface} on device {validDeviceIP}")
                            interfaceOut = sshAccess.send_command(f'show run int {interface}')
                            if snoopTrust in interfaceOut:
                                print(f"INFO: Interface {interface} has configured {snoopTrust} on device {validDeviceIP}")
                                authLog.info(f"Interface {interface} has configured {snoopTrust} on device {validDeviceIP}")
                                vlan1103IntList.append(f"Interface {interface} has configured {snoopTrust}")
                            else:
                                print(f"INFO: Interface {interface} does NOT have configured {snoopTrust} on device {validDeviceIP}")
                                authLog.info(f"Interface {interface} does NOT have configured {snoopTrust} on device {validDeviceIP}")
                                vlan1103IntList.append(f"Interface {interface} does NOT have configured {snoopTrust}")
                    else:
                        print(f"INFO: No interfaces found under {shVlanID1103}")
                        authLog.info(f"No interfaces found under {shVlanID1103}")

                    with open(f"Outputs/{validDeviceIP}_dhcpSnoopCheck.txt", "a") as file:
                        file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                        file.write(f"{vlan1101IntList}\n{vlan1103IntList}")

                except Exception as error:
                    print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
                    authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
                    authLog.debug(traceback.format_exc(),"\n")
       
        except Exception as error:
            print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
            authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
            authLog.debug(traceback.format_exc(),"\n")
            with open(f"failedDevices.txt","a") as failedDevices:
                failedDevices.write(f"User {username} connected to {validDeviceIP} got an error.\n")
        
        finally:
            print(f"Outputs and files successfully created for device {validDeviceIP}.\n")
            print("For any erros or logs please check Logs -> authLog.txt\n")