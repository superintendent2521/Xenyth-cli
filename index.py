import click
import requests
import json
import subprocess
from datetime import datetime
import time
##########################################
#                                       #
#   Python dependencies ^^^^^           #
#            ignore them                #
#                                       #
#                                       #
#                                       #
##########################################
@click.group()
def cli():
    pass

@cli.command()
def services():
    """Get a list of cloud services from the Xenyth dashboard"""

    # Load authentication token from file
    with open('data.json') as f:
        auth_data = json.load(f)
        token = auth_data['token']

    # Set up API endpoint URL and headers
    url = 'https://dashboard.xenyth.net/api/services/cloud/list'
    headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'xenyth-cli/1.0'
    }
    # Make GET request to API and extract relevant fields from response
    response = requests.get(url, headers=headers)
    services = response.json()['cloud']
    for service in services:


        service_hostname = service['service_hostname']
        ip = service['details']['ip']
        ipv6 = service['details']['ipv6']
        service_id = service['id']
        price = service['price']
        service_type_name = service['service_type_name']

        print(f"\nService Hostname: {service_hostname}\nIP: {ip}\nIPv6: {ipv6}\nID: {service_id}\nPrice: {price}\nService Type Name: {service_type_name}\n")



@cli.command()
@click.option('--vmid', type=int, help='Virtual machine ID')
def vmstat(vmid):
    """Get Statistics From a Single VM"""
    # Load authentication token from file
    with open('data.json') as f:
        auth_data = json.load(f)
        token = auth_data['token']

    # Set up API endpoint URL and headers
    url = f'https://dashboard.xenyth.net/api/services/cloud/{vmid}'
    headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'xenyth-cli/1.0'
    }
    # Make GET request to API and extract relevant fields from response
    response = requests.get(url, headers=headers)
    json_response = response.json()

    status = json_response['status']
    service_hostname = json_response['service_hostname']
    service_id = json_response['id']
    price = json_response['price']
    service_type_name = json_response['service_type_name']

    if 'page' in json_response and 'facts' in json_response['page']:
        facts = json_response['page']['facts']
        if 'IP Address' in facts:
            ip = facts['IP Address']['value']
        else:
            ip = None

        if 'IPv6 Address' in facts:
            ipv6 = facts['IPv6 Address']['value']
        else:
            ipv6 = None
    else:
        ip = None
        ipv6 = None

    print(f"Status: {status}\nService Hostname: {service_hostname}\nIP: {ip}\nIPv6: {ipv6}\nID: {service_id}\nPrice: {price}\nService Type Name: {service_type_name}\n")

    return

@cli.command()
def token():
    """Set your token"""

    # Prompt the user for input
    input_str = input("Enter the token: ")

    # Check if the input string is 36 characters long
    if len(input_str) == 36:
        # Read the existing JSON file or create an empty dictionary
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Update the dictionary with the new token value
        data["token"] = input_str

        # Write the updated dictionary to the JSON file
        with open("data.json", "w") as f:
            json.dump(data, f)

        print("Token written to data.json. All commands should work now.")
    else:
        print("Token string is not 36 characters long.")




@cli.command()
def ping():
    """View your ping to Xenyth's servers"""
    hostname = "spdtst.xenyth.net"
    ping = subprocess.Popen(
        ["ping", hostname],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = ping.communicate()
    if error:
        click.echo("Ping Error: {}".format(error.decode("utf-8")))
    else:
        click.echo(out.decode("utf-8"))


@cli.command()
def ticketlist():
    """Lists All Tickets"""
    print("Fetching Ticket info, Please Standby")
    # Load authentication token from file
    with open('data.json') as f:
        auth_data = json.load(f)
        token = auth_data['token']

    # Set up API endpoint URL and headers
    url = f'https://dashboard.xenyth.net/api/tickets/list'
    headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'xenyth-cli/1.0'
    }
    # Make GET request to API and extract relevant fields from response
    response = requests.get(url, headers=headers)
    print("this can and will flood your terminal if you have large ammounts of tickets as it shows EVERY ticket That was opened/closed, You have been warned and there is a 3 second wait")
    time.sleep(2)
    if response.status_code == 200:
        json_response = response.json()

        # Iterate through the list of tickets and print the desired fields
        for ticket in json_response:
            ticket_id = ticket['id']
            status = ticket['status']
            status_text = ticket['statustext']
            title = ticket['title']
           

            print(f"ID: {ticket_id}")
            print(f"Status: {status}")
            print(f"Status Text: {status_text}")
            print(f"Title: {title}")
            print("\n")
    else:
        print("Error: Unable to fetch ticket information.")


@cli.command()
@click.option('--ticket', type=int, help='Ticket ID')

def ticketinfo(ticket):
    """Get Ticket Thread info"""
    # Load authentication token from file
    with open('data.json') as f:
        auth_data = json.load(f)
        token = auth_data['token']

    # Set up API endpoint URL and headers
    url = f'https://dashboard.xenyth.net/api/tickets/{ticket}'
    headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'xenyth-cli/1.0'
} 

    # Make GET request to API and extract relevant fields from response
    response = requests.get(url, headers=headers)
    json_response = response.json()

    # Print required fields
    print(f"ID: {json_response['id']}")
    print(f"Status Text: {json_response['statustext']}")
    print(f"Title: {json_response['title']}")
    print(f"Agent: {json_response['agent']}")

    # Print replies with content and author
    print("\nReplies:")
    for reply in json_response['replies']:
        print(f"Content: {reply['content']}")
        print(f"Author: {reply['author']}")
        print()

#stfu python no one loves you
if __name__ == '__main__':
    cli()

