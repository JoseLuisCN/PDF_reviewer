# Copyright (C) 2023-2025 Cognizant Digital Business, Evolutionary AI.
# All Rights Reserved.
# Issued under the Academic Public License.
#
# You can be released from the terms, and requirements of the Academic Public
# License by purchasing a commercial license.
# Purchase of a commercial license is mandatory for any use of the
# neuro-san-studio SDK Software in commercial settings.
#
import os
import uuid
import csv
from typing import Any
from typing import Dict
from typing import Union

from neuro_san.interfaces.coded_tool import CodedTool


class IncidentDBTool(CodedTool):
    """
    CodedTool implementation that logs customer incidents such as delays,
    missed flights, and baggage issues. Each incident is stored in a CSV file
    and assigned a unique incident ID.
    """

    def __init__(self):
        self.name = "IncidentDBTool"
        self.incident_log = {}
        self.csv_file = "coded_tools/air_europe_demo/db/customer_incidents.csv"

        # Ensure the CSV file exists with headers
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "incident_id", "customer_name", "issue_type",
                    "description", "status", "escalated"
                ])

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary with the following keys:
            - "customer_name" (str): The full name of the customer.
            - "issue_type" (str): The type of incident (e.g., 'Delayed Flight').
            - "description" (str): A detailed description of the incident.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
            but whose values are meant to be kept out of the chat stream.

        :return:
            If successful:
                A dictionary containing:
                - "incident_id": The unique ID assigned to the incident.
                - "message": Confirmation message.
                - "details": The full incident data.
            Otherwise:
                A text string error message in the format:
                "Error: <error message>"
        """
        customer = args.get("customer_name")
        issue_type = args.get("issue_type")
        description = args.get("description")

        if not all([customer, issue_type, description]):
            return "Error: Missing required incident details."

        incident_id = str(uuid.uuid4())
        incident_data = {
            "customer_name": customer,
            "issue_type": issue_type,
            "description": description,
            "status": "Logged",
            "escalated": False
        }

        self.incident_log[incident_id] = incident_data

        # Append the incident to the CSV file
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                incident_id,
                incident_data["customer_name"],
                incident_data["issue_type"],
                incident_data["description"],
                incident_data["status"],
                incident_data["escalated"]
            ])

        return {
            "incident_id": incident_id,
            "message": "Incident successfully logged.",
            "details": self.incident_log[incident_id]
        }