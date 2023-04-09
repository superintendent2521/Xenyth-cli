import click
import requests
import json
import subprocess



return
hasseen()
@click.group()
def cli():
    pass

@cli.command()
def services():
    """Get a list of cloud services from the Xenyth dashboard API"""

    # Load authentication token from file
    with open('data.json') as f:
        auth_data = json.load(f)
        token = auth_data['token']

    # Set up API endpoint URL and headers
    url = 'https://dashboard.xenyth.net/api/services/cloud/list'
    headers = {'Authorization': f'Bearer {token}'}

    # Make GET request to API and extract relevant fields from response
    response = requests.get(url, headers=headers)
    services = response.json()['cloud']
    for service in services:

        vmtype = type['type']
        service_hostname = service['service_hostname']
        ip = service['details']['ip']
        ipv6 = service['details']['ipv6']
        service_id = service['id']
        price = service['price']
        service_type_name = service['service_type_name']

        print(f"Status: {vmtype}\nService Hostname: {service_hostname}\nIP: {ip}\nIPv6: {ipv6}\nID: {service_id}\nPrice: {price}\nService Type Name: {service_type_name}\n")



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
    headers = {'Authorization': f'Bearer {token}'}

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
        print("Input string is not 36 characters long.")




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
if __name__ == '__main__':
    cli()
