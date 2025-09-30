from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import *
import json
import time
import logging

logger = logging.getLogger(__name__)

class Spreadsheet: 

    def __init__(self,env,creds):
        self._creds   = creds
        self._env= env
        self._service = None
        self._build_service()

    @property
    def sheet(self):
        return self.service.spreadsheets()
    
    @property
    def creds(self)->None:
        if not isinstance(self._creds,Credentials):
            self._auth()
        return self._creds

    def _build_service(self,sheet='sheets',version='v4')->None:
        logger.debug(f"Build Google Sheet service sheet:'{sheet}' version:'{version}'")
        try:
            self._service = build(
                sheet,
                version,
                credentials=self.creds,
                cache_discovery=False
            )
        except Exception as e:
            logger.error(f"Build GoogleSheet service error: {e}")
            self._service = None

    def _auth(self)->None:
        creds = self._creds
        try:
            if isinstance(creds,str):
                creds = json.loads(creds)
            self._creds = Credentials.from_service_account_info(creds, scopes=self._env.get("SCOPES",[]))
        except Exception as e:
            logger.error(f"Authorization Failure:{e},creds:{creds}")
            time.sleep(2)

    def _fetch_sheet(self,sheet_name:str,sheet_id:str,begin:int=1,end:int=100000)->List:
        sheet = self._service.spreadsheets()
        range= f"{sheet_name}!{begin}:{end}"
        logger.debug(f"Search row: {range}")
        try:
            result = sheet.values().get(
                spreadsheetId=sheet_id,
                range=range
                ).execute()

        except Exception as e:
            logger.error(f"Error occured during row fetching: {e}")
            result = {}
        return result.get("values", [])