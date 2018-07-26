import logging
import datetime
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np

# Create a custom logging level to display more info in
# the terminal than in the log file.
logging.LEVEL_INFO_CH = 15
logging.addLevelName(logging.LEVEL_INFO_CH, "info_ch")
def info_ch(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(logging.LEVEL_INFO_CH):
        self._log(logging.LEVEL_INFO_CH, message, args, **kws)
logging.Logger.info_ch = info_ch

logging.LEVEL_DEBUG_COM = 7
logging.addLevelName(logging.LEVEL_DEBUG_COM, "debug_com")
def debug_com(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(logging.LEVEL_DEBUG_COM):
        self._log(logging.LEVEL_DEBUG_COM, message, args, **kws)
logging.Logger.debug_com = debug_com

separator_title = "--------------------------------------------------------------------------------"

legit_keys = ["critical", "debug", "error", "info", "warning", "info_ch", "debug_com"]
legit_keys += [key.upper() for key in legit_keys]

LOG_folder = '..\\_logs'
LOG_name = 'Main'

class LOG_Manager() :
    """
    Class used to handle logs.
    The first time that this class is instancied, we need to start the log manager
    by using the method start(). Once it's done, new log entry can be send by using
    the send() method.
    If we need to add log entries in another file, NO NEED to apply start() a second
    time. We need only to instanciate a new LOG_Manager.

    LEVEL :
    In order to add an entry to the log, we need at least one parameter : the entry 'level'.
    It corresponds to the "urgency" of the message. It can be anything contained in "legit_keys".

    HANDLERS :
    By default, the LOG_Manager set two channels (called handlers in logging module) :
        - ConsoleHandler send message directly in the terminal
        - FileHandler append the message in a file that change everyday.

    HANDLERS + LEVEL :
    A message is print into a handler only if the message-level is superior or equal to the
    handler-level (defined by level_console, and level_file).
    By default, we want to print only messages with priority above "INFO".
    However, it is possible to set the handlers in the "DEBUG" level, where they will
    lots of text usefull to the debugging.
    """
    def __init__(self) :
        pass

    def start(self, **kwargs) :
        """
        Start the LOG_Manager.
        This function need to be called only ONE time in a ipython terminal.

        NOTE :
            - legit level are (sorted by priority) :
                >> logging.DEBUG >> logging.LEVEL_INFO_CH >> logging.INFO >> logging.WARNING
                >> logging.ERROR >> logging.CRITICAL
        INPUT :
            - [int]   level_console : Console-handler level (LEVEL_INFO_CH by default).
            - [int]   level_file    : File-handler level (INFO by default).

        OUTPUT :
            - None
        """
        # Get all the parameters
        level_console   = get_value("level_console" , kwargs, logging.LEVEL_INFO_CH)
        level_file      = get_value("level_file"    , kwargs, logging.INFO)

        # Filename management
        now = datetime.datetime.now()
        folder = os.path.join(LOG_folder,now.strftime("%Y-%m"))
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename =  folder + "\\" + now.strftime("%Y-%m-%d") + ".log"

        # Get logger
        logger = logging.getLogger(LOG_name)

        # Configure logger if necessary
        if logger.handlers == [] :
            formatter = logging.Formatter(  fmt = '%(asctime)s >> %(levelname)8s >> %(message)s',
                                            datefmt = "%Y-%m-%d , %H:%M:%S")

            # -- Create FILE handler
            fh = logging.FileHandler(filename)
            fh.setLevel(level_file)
            fh.setFormatter(formatter)

            # -- Create CONSOLE handler
            # -- It is already instancied by basicConfig on ManuPC, universal behavior ?
            # ch = logging.StreamHandler()
            # ch.setLevel(level_console)
            # ch.setFormatter(formatter)

            # -- Add the handlers to the logger
            logger.addHandler(fh)
            # logger.addHandler(ch)

        # Basic config
        # -- In fact, it is the CONSOLE HANDLER !
        logging.basicConfig(level = level_console,
                    format = '%(asctime)s >> %(levelname)8s >> %(message)s',
                    datefmt = "%Y-%m-%d , %H:%M:%S" )

    def send(self, **kwargs) :
        """
        Send an entry to the logs.

        EXAMPLE :
            - self.send(level="info", message="this is a regular info msg.")
            - self.send(level="info", message="this is a title.", title = True)
            - self.send(level="warning", message = "Warning with context.", context = "driver")

        INPUT :
            - [int]   level         : Console-handler level (LEVEL_INFO_CH by default).
            - [str]   messages      : File-handler level (INFO by default).
            - [bool]  title         : if True, the msg is printed as a title (FALSE by default).
            - [str]   context       : Add prefix "[context]" at the message (nothing by default).

        OUTPUT :
            - None
        """
        # Get parameters
        level = get_value("level", kwargs, "info")
        message = get_value("message", kwargs, "")
        title = get_value("title", kwargs, False)
        context = get_value("context", kwargs, False)

        # Add context to the message (e.g : " [LABVIEW] ")
        if context :
            message = "[" + context.upper() + "] " + message

        # Send message
        if level in legit_keys :
            # -- Get he good method to call depending on the asked level
            logger = logging.getLogger(LOG_name)
            module = getattr(logger, level.lower())
            # -- Format the message as a TITLE if asked ...
            if title :
                spacing = 78/2 - len(message)/2
                module(separator_title)
                module(" "*spacing + message.upper())
                module(separator_title)
            # -- ... or keep it like this.
            else :
                module(message)
        # Raise a warning if log level is not understood and discard message.
        else :
            self.send("warning", "%s is not a valid log key. Message is discarded.")

def get_value(name, dict, default_value) :
    """
    Return "dict[name]" if exists, "default_value" otherwise.
    """
    if name in dict :
        value = dict[name]
    else :
        value = default_value
    return value

if __name__ == "__main__" :
    log = LOG_Manager()
    log.start()

    log.send(level="info", message="text test oipo", title = True)
    for i in range(10) :
        log.send(level="warning", message="text test" + str(i))

    for i in legit_keys :
        log.send(level=i, message="text test oipo", context = "popol")
