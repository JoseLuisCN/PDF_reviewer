# Copyright (C) 2023-2025 Cognizant Digital Business, Evolutionary AI.
# All Rights Reserved.
# Issued under the Academic Public License.
#
# You can be released from the terms, and requirements of the Academic Public
# License by purchasing a commercial license.
# Purchase of a commercial license is mandatory for any use of the
# neuro-san-studio SDK Software in commercial settings.
#
from typing import Any
from typing import Dict
from typing import Union

from neuro_san.interfaces.coded_tool import CodedTool


class URLProvider_AE(CodedTool):
    """
    CodedTool implementation which provides URLs for airline's helpdesk and intranet resources.
    """

    def __init__(self):
        """
        Constructs a URL Provider for airline's intranet.
        """
        self.airline_policy_urls = {
            "Customer Service": "https://www.aireuropa.com/es/en/aea/customer-service.html",
            "Group request reservation": "https://www.aireuropa.com/es/en/group-bookings?_gl=1*1riw0t3*_up*MQ..*_ga*MjAwNDE4NjQ0Ny4xNzU0OTE0ODgx*_ga_3FP4QGJ6VF*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTQ4ODEkajYwJGwwJGgw*_ga_G13VWM48QC*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTQ4ODEkajYwJGwwJGgyOTU2NzY4Nzk.",
            "Flight notices": "https://www.aireuropa.com/es/en/aea/press-releases/anuncios.html?_gl=1*1o0ang*_up*MQ..*_ga*MjAwNDE4NjQ0Ny4xNzU0OTE0ODgx*_ga_3FP4QGJ6VF*czE3NTQ5MTQ4ODEkbzEkZzEkdDE3NTQ5MTQ5MzgkajMkbDAkaDA.*_ga_G13VWM48QC*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTQ5MzkkajIkbDAkaDI5NTY3Njg3OQ..",
            "Access your booking": "https://www.aireuropa.com/es/en/mytrips?_gl=1*j415ka*_up*MQ..*_ga*MjAwNDE4NjQ0Ny4xNzU0OTE0ODgx*_ga_3FP4QGJ6VF*czE3NTQ5MTQ4ODEkbzEkZzEkdDE3NTQ5MTUwMTgkajIzJGwwJGgw*_ga_G13VWM48QC*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTUwMTgkajIzJGwwJGgyOTU2NzY4Nzk.",
            "Baggage: Everything You Need to Know": "https://www.aireuropa.com/es/en/aea/travel-information/baggage.html?_gl=1*uivniz*_up*MQ..*_ga*MjAwNDE4NjQ0Ny4xNzU0OTE0ODgx*_ga_3FP4QGJ6VF*czE3NTQ5MTQ4ODEkbzEkZzEkdDE3NTQ5MTUwNzgkajYwJGwwJGgw*_ga_G13VWM48QC*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTUwNzgkajYwJGwwJGgyOTU2NzY4Nzk.",
            "Terms and Conditions": "https://www.aireuropa.com/es/en/aea/travel-information/terms-and-conditions.html?_gl=1*k6yo79*_up*MQ..*_ga*MjAwNDE4NjQ0Ny4xNzU0OTE0ODgx*_ga_3FP4QGJ6VF*czE3NTQ5MTQ4ODEkbzEkZzEkdDE3NTQ5MTUwOTYkajQyJGwwJGgw*_ga_G13VWM48QC*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTUwOTYkajQyJGwwJGgyOTU2NzY4Nzk.",
            "Air Europa's services": "https://www.aireuropa.com/es/en/aea/aexperience/services.html?_gl=1*1lhhan0*_up*MQ..*_ga*MjAwNDE4NjQ0Ny4xNzU0OTE0ODgx*_ga_3FP4QGJ6VF*czE3NTQ5MTQ4ODEkbzEkZzEkdDE3NTQ5MTUxOTkkajYwJGwwJGgw*_ga_G13VWM48QC*czE3NTQ5MTQ4ODEkbzEkZzAkdDE3NTQ5MTUxOTkkajYwJGwwJGgyOTU2NzY4Nzk.",
            "Top Sales": "https://www.aireuropa.com/es/en/aea/offers.html?_gl=1*znceu*_up*MQ..*_ga*MTE4MTY0NDgwMy4xNzU0OTc5Njc4*_ga_3FP4QGJ6VF*czE3NTQ5Nzk2NzgkbzEkZzEkdDE3NTQ5Nzk2OTIkajQ2JGwwJGgw*_ga_G13VWM48QC*czE3NTQ5Nzk2NzgkbzEkZzAkdDE3NTQ5Nzk2OTIkajQ2JGwwJGgxNjM0NDYzMDU3",
            "Find Flights Tickets and Deals":"https://www.aireuropa.com/en-es/flight-deals?em_o=MAD&_gl=1*1uy9yxy*_up*MQ..*_ga*MTM3NzU1NTI2Mi4xNzU0OTgwNTA1*_ga_3FP4QGJ6VF*czE3NTQ5ODA1MDQkbzEkZzAkdDE3NTQ5ODA1MDQkajYwJGwwJGgw*_ga_G13VWM48QC*czE3NTQ5ODA1MDQkbzEkZzAkdDE3NTQ5ODA1MDQkajYwJGwwJGg2Mjk4NDk4NDg."
        }

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "app_name" the name of the Airline Policy for which the URL is needed.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
                but whose values are meant to be kept out of the chat stream.

                This dictionary is largely to be treated as read-only.
                It is possible to add key/value pairs to this dict that do not
                yet exist as a bulletin board, as long as the responsibility
                for which coded_tool publishes new entries is well understood
                by the agent chain implementation and the coded_tool implementation
                adding the data is not invoke()-ed more than once.

                Keys expected for this implementation are:
                    None

        :return:
            In case of successful execution:
                The URL to the policy as a string.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """
        app_name: str = args.get("app_name", None)
        if app_name is None:
            return "Error: No app name provided."
        print(">>>>>>>>>>>>>>>>>>>URL Provider>>>>>>>>>>>>>>>>>>")
        print(f"App name: {app_name}")
        app_url = self.airline_policy_urls.get(app_name)
        print(f"URL: {app_url}")
        print(">>>>>>>>>>>>>>>>>>>DONE !!!>>>>>>>>>>>>>>>>>>")
        return app_url