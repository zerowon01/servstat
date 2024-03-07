import requests
from requests.exceptions import MissingSchema
import click
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
import json
import warnings
from importlib import metadata
warnings.filterwarnings("ignore")


def check_status_page(site):
    pass

def print_status_page(site, show_failed_site=False):
    output = site.Service + ": "#.rjust(20)

    try:
        resp = requests.get(site.URL)
        #Evaluate via JSON response
        if site.Format == "json":
            normalstatus_pair = list(json.loads(site.NormalStatus).items())[0]
            #Get the kv pair defined in "NormalStatus"
            #And see if the value for the key in the response matched the NormalStatus value
            if resp.json()[normalstatus_pair[0]] == normalstatus_pair[1]:
                output = output.ljust(18) + click.style(" ●", fg="green")
            else:
                output = output.ljust(18) + click.style(" X", fg="red")
        #Evaluate via HTML content
        else:
            soup = BeautifulSoup(resp.content)
            if site.NormalStatus.lower() in str(soup).lower():
                output = output.ljust(18) + click.style(" ●", fg="green") 
            else:
                output = output.ljust(18) + click.style(" X", fg="red")
                if show_failed_site:
                    click.launch(site.URL)
    except (AttributeError, MissingSchema) as e:
        output = output.ljust(18) + click.style("▲", fg="yellow")
    click.echo(output)


# @click.version_option(pkg_resources.get_distribution("service_status").version)
@click.version_option(metadata.version("servstat"))
@click.command()
@click.option("--file")
@click.option("--show_failed_site", is_flag=True)
@click.option("--json_format", is_flag=True)
@click.option("--export_csv", is_flag=True)
def cli(file, json_format: bool, export_csv:bool, show_failed_site:bool):
    print("Checking system status for various sites")
    df = pd.read_csv(file)  
    for site in list(df.iterrows()):

        #Check for any nan columns for the site
        if any(site[1].isna()):
            output = f"{site[1].Service}: "
            output = output.ljust(18) + click.style(" ▲", fg="yellow")
            click.echo(output)
            continue

        #TODO: Refactor to separate CHECK and PRINT (abstract into OUTPUT)
        print_status_page(site[1], show_failed_site)


if __name__ == "__main__":
    cli()
