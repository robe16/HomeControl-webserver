from datetime import datetime
import logging
import os

# Logging Level Values:
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
#  UNSET     0

logfile = os.path.join(os.path.dirname(__file__), 'webserver.log')
logging.basicConfig(filename=logfile, level=20)

timeformat = '%d/%m/%Y %H:%M:%S.%f'

def create_device_log_message(command, device_type, dvc_ip, response):
    return _add_timestamp("'{command}' request sent to {device_type}{dvc_ip} - {response}".format(command=command.replace('/r',''),
                                                                                                  device_type=device_type,
                                                                                                  dvc_ip=' '+dvc_ip,
                                                                                                  response=response))


def log_error(error_msg, dvc_id=''):
    log_msg = _create_msg(error_msg, dvc_id=dvc_id)
    _log(log_msg, level=40)


def log_warning(error_msg, dvc_id=''):
    log_msg = _create_msg(error_msg, dvc_id=dvc_id)
    _log(log_msg, level=30)


def log_general(msg, dvc_id=''):
    log_msg = _create_msg(msg, dvc_id=dvc_id)
    _log(log_msg, level=20)


def _log(log_msg, level=20):
    if level == 50:
        logging.critical(log_msg)
    elif level == 40:
        logging.error(log_msg)
    elif level == 30:
        logging.warning(log_msg)
    elif level == 20:
        logging.info(log_msg)
    else:
        logging.debug(log_msg)


def _create_msg(msg, dvc_id=''):
    if dvc_id:
        msg += ' - ' + dvc_id
    return _add_timestamp('{msg}'.format(msg=msg))


def _add_timestamp(log_msg):
    return '{timestamp} - {log_msg}'.format(timestamp=datetime.now().strftime(timeformat),
                                            log_msg=log_msg)
