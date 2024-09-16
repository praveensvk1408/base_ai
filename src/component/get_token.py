
import requests
import pytest
from requests.auth import HTTPBasicAuth
class GetToken():
    def __init__(self):
        self.token_url = "https://auth-sqa.sssiotpfs.com/oauth2/default/v1/token"
        self.cleint_id = "0oagplyjar2nouTw51d7"
        self.secret = "3bGjJGK6MrFE7hpeQa506bgttf5SByWq4jz3bSv05i8t6u40ODIRtf0cc2BbOxzL"
    
    def get_token(self):
        form_data = {
        'grant_type': 'client_credentials',
        'scope': 'system'
        }
        response = requests.post(self.token_url, data=form_data, auth=HTTPBasicAuth(self.cleint_id, self.secret), timeout=5)
        response.raise_for_status()
        return response
