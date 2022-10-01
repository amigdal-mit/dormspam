import os
os.chdir(os.environ['HOME'] + '/Scripts/dormspam/backend')

from server.emails.parse import parse_email
import sys

sys.stdin.reconfigure(encoding='latin-1')

event = parse_email(sys.stdin.read())
if (event is not None):
    print(event.json())
    exit(0)
else:
    print("could not parse email")
    exit(1)
