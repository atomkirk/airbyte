# import sys
# import os
# parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# # Add the ptdraft folder path to the sys.path list
# sys.path.append(parent_dir_name)


import base64
import hmac
import hashlib
import pyodbc
import time
import random
import string
from datetime import datetime
from typing import Mapping, Any
from .errors import (
  NETSUITE_DRIVER_NOT_FOUND_ERROR,
  AIRBYTE_ODBC_DRIVER_DOES_NOT_EXIST_ERROR,
  NETSUITE_INCORRECT_PASSWORD,
  AIRBYTE_ODBC_DRIVER_INCORRECT_PASSWORD_ERROR,
  NETSUITE_HOST_RESOLUTION_FAILURE,
  AIRBYTE_ODBC_DRIVER_HOST_RESOLUTION_FAILURE
)


class NetsuiteODBCCursorConstructor:
  def generate_nonce(self) -> str:
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits
    # Generate a random 10-character string
    random_string = ''.join(random.choice(characters) for i in range(10))
    return random_string
  
  def generate_timestamp(self) -> str:
    time_tuple = datetime.now().timetuple() 
    return str(time.mktime(time_tuple))[0:10]
    
  def construct_password(self, config: Mapping[str, Any]) -> str:

    timestamp = self.generate_timestamp()
    nonce = self.generate_nonce()

    base_string = config['account_id'] + '&' + config['consumer_key'] + '&' + config['token_key'] + '&' + nonce + '&' + timestamp

    key = config['consumer_secret'] + '&' + config['token_secret']

    hmac_sha256 = hmac.new(key.encode(), base_string.encode(), hashlib.sha256)

    # Compute the HMAC and encode the result in Base64
    hmac_base64 = base64.b64encode(hmac_sha256.digest())

    hmac_base64_str = hmac_base64.decode()

    return base_string + '&' + hmac_base64_str + '&HMAC-SHA256'
  
  def construct_db_string(self, config: Mapping[str, Any]) -> str:
    password = self.construct_password(config)
    connection_string = f'DRIVER=NetSuite ODBC Drivers 8.1;Host={config["service_host"]};Port={config["service_port"]};Encrypted=1;AllowSinglePacketLogout=1;Truststore=/opt/netsuite/odbcclient/cert/ca3.cer;ServerDataSource=NetSuite2.com;UID=TBA;PWD={password};CustomProperties=AccountID={config["account_id"]};RoleID=57;StaticSchema=1'
    return connection_string

    
  def create_database_cursor(self, config: Mapping[str, Any]) -> pyodbc.Cursor:
    connection_string = self.construct_db_string(config)
    try:
      cxn = pyodbc.connect(connection_string)
      return cxn.cursor()
    except Exception as e:
      message = str(e)
      if NETSUITE_DRIVER_NOT_FOUND_ERROR in message:
        raise Exception(AIRBYTE_ODBC_DRIVER_DOES_NOT_EXIST_ERROR)
      elif NETSUITE_INCORRECT_PASSWORD in message:
        raise Exception(AIRBYTE_ODBC_DRIVER_INCORRECT_PASSWORD_ERROR)
      elif NETSUITE_HOST_RESOLUTION_FAILURE in message:
        raise Exception(AIRBYTE_ODBC_DRIVER_HOST_RESOLUTION_FAILURE)
      else:
        raise e
