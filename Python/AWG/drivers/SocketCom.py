# -*- coding: utf-8 -*-
import socket
import re
from six import string_types
# from Utility.print_functions import *

from _logs.logs import LOG_Manager
log = LOG_Manager()

def test():
    sock=SocketCom('192.168.137.2',4000)
    sock.openCom()
    sock.sendMessage('WLIST:SIZE?')
    ansr=sock.readMessage()

    msg=[]
    for i in xrange (1,int(ansr)+1):
       msg.append('WLIST:NAME? '+str(i))
    sock.sendMessage(msg)
    wnames=sock.readMessage()

    LWNames = re.findall('"waveseq.*?"',wnames)

    dlmsg=[]
    for name in LWNames:
        dlmsg.append('WLISt:WAVeform:DELete '+name)
    sock.sendMessage(dlmsg)

    sock.closeCom()


class SocketCom(object):
    """
    General Communication class for messages delimited by Delimiter and ended
    by EndOfMessage to interface (Tektronix AWG) devices.
    """

    def __init__(self, **kwargs):
        """Define SocketCom"""
        super(SocketCom, self).__init__()

        # IP
        if "Ip" in kwargs.keys():
            self.TCP_IP = kwargs["Ip"]
            self.isTCP_IP_set = True
        else:
            self.isTCP_IP_set = False

        # Port
        if "Port" in kwargs.keys():
            self.TCP_PORT = kwargs["Port"]
            self.isTCP_PORT_set = True
        else:
            self.isTCP_PORT_set = False

        # Delimiter
        if "Delimiter" in kwargs.keys():
            self.delimiter = kwargs["Delimiter"]
        else:
            self.delimiter = ';:'

        # EndOfMessage
        if "EndOfMessage" in kwargs.keys():
            self.msgEnd = kwargs["EndOfMessage"]
        else:
            self.msgEnd = '\n'

        # General settings
        self.isComOpened = False
        self.BUFFER_SIZE = 8*1024

    def set_Ip(self, Ip):
        self.TCP_IP = Ip
        self.isTCP_IP_set = True

    def set_Port(self, Port):
        self.TCP_PORT = int(Port)
        self.isTCP_PORT_set = True

    def open_communication(self, runtype):
        """
        Start a socket
        Connect.
        NOTE: runtype should contain
            awg_tcpip_enabled = True
            tprint_enabled = False
            awg_non_authorized_ip = []
        """
        msg = ""
        if self.isTCP_IP_set:
            ip_msg = self.TCP_IP
        else:
            ip_msg = "no IP provided"

        # Check that runtype contains the required properties.
        if not runtype.isproperty("awg_tcpip_enabled"):
            log.send(level="critical",
                     context="SocketCom.open_communication",
                     message="awg_tcpip_enabled not defined in runtype.")
            raise ValueError("awg_tcpip_enabled not defined in runtype.")
        if not runtype.isproperty("awg_non_authorized_ip"):
            log.send(level="critical",
                     context="SocketCom.open_communication",
                     message="awg_non_authorized_ip not defined in runtype.")
            raise ValueError("awg_non_authorized_ip not defined in runtype.")

        # Check the authorizations
        if runtype.get("awg_tcpip_enabled") and\
                (self.TCP_IP not in runtype.get("awg_non_authorized_ip")):

            if self.isTCP_IP_set and self.isTCP_PORT_set:
                # Start socket
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect socket
                self.s.connect((self.TCP_IP, self.TCP_PORT))
                self.s.settimeout(300)
                self.isComOpened = True

                # Log
                log.send(level="debug_com",
                         context="SocketCom.open_communication",
                         message="done: {}.".format(ip_msg))
            else:
                log.send(level="critical",
                         context="SocketCom.open_communication",
                         message="{}".format(ip_msg))
                raise ValueError("IP or Port not define.")

    def close_communication(self, runtype):
        """
        Close the socket. All future operations on the socket object will fail.
        The remote end will receive no more data
        (after queued data is flushed).
        Sockets are automatically closed when they are garbage-collected.
        """

        # Check that runtype contains the required properties.
        if not runtype.isproperty("awg_tcpip_enabled"):
            log.send(level="critical",
                     context="SocketCom.close_communication",
                     message="awg_tcpip_enabled not defined in runtype.")
            raise ValueError("awg_tcpip_enabled not defined in runtype.")
        if not runtype.isproperty("awg_non_authorized_ip"):
            log.send(level="critical",
                     context="SocketCom.close_communication",
                     message="awg_non_authorized_ip not defined in runtype.")
            raise ValueError("awg_non_authorized_ip not defined in runtype.")

        # Check the authorizations
        if runtype.get("awg_tcpip_enabled") and\
                (self.TCP_IP not in runtype.get("awg_non_authorized_ip")):
            self.s.close()
            self.isComOpened = False

            log.send(level="debug_com",
                     context="SocketCom.close_communication",
                     message="done.")
        else:
            log.send(level="critical",
                     context="SocketCom.close_communication",
                     message="{}".format(ip_msg))
            raise ValueError("IP or Port not define.")

    def send_message(self, msg, runtype):
        """
        Send a message to the machine
        Accepts either a string or a list of strings as msg.
        """
        # Check that runtype contains the required properties.
        # print runtype.values
        if not runtype.isproperty("awg_tcpip_enabled"):
            msg = "awg_tcpip_enabled not defined in runtype."
            log.send(level="critical",
                     context="SocketCom.send_message",
                     message=msg)
            raise ValueError(msg)
        if not runtype.isproperty("awg_non_authorized_ip"):
            msg = "awg_non_authorized_ip not defined in runtype."
            log.send(level="critical",
                     context="SocketCom.send_message",
                     message=msg)
            raise ValueError(msg)

        if isinstance(msg, basestring):
            # Check the authorizations
            if runtype.get("awg_tcpip_enabled") and\
                    (self.TCP_IP not in runtype.get("awg_non_authorized_ip")):
                self.s.send(msg+self.msgEnd)
                # Log
                log.send(level="debug_com",
                         context="SocketCom.send_message",
                         message="{}".format(msg))
        else:
            try:
                fullMsg = ''
                for msgPart in msg:
                    fullMsg = fullMsg + msgPart + self.delimiter
                fullMsg.rstrip(self.delimiter)

                # Check the authorizations
                if runtype.get("awg_tcpip_enabled") and\
                        (self.TCP_IP not in \
                        runtype.get("awg_non_authorized_ip")):
                    self.s.send(fullMsg+self.msgEnd)
                    # Log
                    log.send(level="debug_com",
                             context="SocketCom.send_message",
                             message="{}".format(msg))

            except TypeError:
                msg = 'TypeError occourred on message text, please ensure \
                      that message is a string or a list of strings'
                log.send(level="critical",
                         context="SocketCom.send_message",
                         message="{}".format(msg))

    def read_message(self, runtype):
        """Read message."""
        # Check that runtype contains the required properties.
        if not runtype.isproperty("awg_tcpip_enabled"):
            msg = "awg_tcpip_enabled not defined in runtype."
            log.send(level="critical",
                     context="SocketCom.send_message",
                     message=msg)
            raise ValueError(msg)
        if not runtype.isproperty("awg_non_authorized_ip"):
            msg = "awg_non_authorized_ip not defined in runtype."
            log.send(level="critical",
                     context="SocketCom.send_message",
                     message=msg)
            raise ValueError(msg)

        msg = ""

        # Check the authorizations
        if runtype.get("awg_tcpip_enabled") and\
                (self.TCP_IP not in runtype.get("awg_non_authorized_ip")):
            cont = 1
            dat = ''
            while cont:
                dat = dat + self.s.recv(self.BUFFER_SIZE)
                if dat.endswith(self.msgEnd):
                    cont = 0
            msg = dat.rstrip(self.msgEnd)
        else:
            msg += 'nothing to listen to'

        # Log
        log.send(level="debug_com",
                 context="SocketCom.read_message",
                 message="{}".format(msg))

        return msg


if __name__ == '__main__':
    test()
