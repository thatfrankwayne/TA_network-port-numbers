"""
TA_network_port_numbers
refresh-lookup.py
Updates the iana-ports-and-transports.csv lookup from IANA.
"""

from codecs import iterdecode
from contextlib import closing
import csv
import requests
import sys


IANA_PROTOCOLS_LINK = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"


table = {}


def make_table_from_iana_registry():
    # return "service-names-port-numbers.csv"
    try:
        with closing(requests.get(IANA_PROTOCOLS_LINK)) as req:
            registry = req.text.split("\r\n")
        registry = [i.replace("\n", "") for i in registry]
        reader = csv.DictReader(registry)
    except Exception as e:
        sys.stderr.write(f"Fatal {e} {type(e)}\n")
        exit(1)

    try:
        for row in reader:
            service = row["Service Name"].strip()
            port = row["Port Number"].strip()
            transport = row["Transport Protocol"].strip()
            description = row["Description"].strip()
            if description != "Unassigned" and port.isdigit() and len(transport) > 0:
                k = (int(port), transport)
                if k not in table:
                    table[k] = (service, description)
    except Exception as e:
        sys.stderr.write(f"Fatal {e} {type(e)}\n")
        exit(1)


def write_table_to_stdout() -> None:
    global table
    sys.stdout.write("iana_port,iana_transport,iana_service,iana_description\n")
    for k in sorted(table.keys()):
        sys.stdout.write(f"{k[0]},\"{k[1]}\",\"{table[k][0]}\",\"{table[k][1]}\"\n")


def main():
    make_table_from_iana_registry()
    write_table_to_stdout()


if __name__ == "__main__":
    main()
