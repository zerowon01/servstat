import requests
from requests.exceptions import MissingSchema
import click
import pandas as pd
from bs4 import BeautifulSoup
import warnings
from importlib import metadata
warnings.filterwarnings("ignore")


def check_status_page(site):
    pass

def print_status_page(site):
    output = site.Service + ": "#.rjust(20)
    try:
        resp = requests.get(site.URL)
        soup = BeautifulSoup(resp.content)
        output = output.ljust(18) + (click.style(" ●", fg="green") if site.NormalStatus.lower() in str(soup).lower() else click.style(" X", fg="red"))
    except (AttributeError, MissingSchema) as e:
        output = output.ljust(18) + click.style("▲", fg="yellow")
    click.echo(output)


# @click.version_option(pkg_resources.get_distribution("service_status").version)
@click.version_option(metadata.version("servstat"))
@click.command()
@click.option("--file")
@click.option("--json_format", is_flag=True)
@click.option("--export_csv", is_flag=True)
def cli(file, json_format, export_csv):
    print("Checking system status for various sites")
    df = pd.read_csv(file)  
    for site in list(df.iterrows()):
        # print(site[1].Service )
        if any(site[1].isna()):
            output = f"{site[1].Service}: "
            output = output.ljust(18) + click.style(" ▲", fg="yellow")
            click.echo(output)
            continue

        #TODO: Refactor to separate CHECK and PRINT (abstract into OUTPUT)
        print_status_page(site[1])


if __name__ == "__main__":
    cli()
