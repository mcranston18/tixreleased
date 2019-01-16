import os, requests

BASE_URL = os.getenv("TM_URL")


class TicketFinder:
    def __init__(self, event_id="100054EC0AF5CE9E"):
        self.event_id = event_id

    def handle_success(self, response):
        json_response = response.json()

        return {
            "total": json_response["total"],
            "picks": json_response["picks"],
            "sections": json_response["sections"],
        }

    def handle_error(self, response):
        return {
            "error": True,
            "status_code": response.status_code,
            "response": response.json(),
        }

    def get_availability(self):
        url = BASE_URL
        response = requests.get(url)

        if response.status_code == 200:
            try:
                return self.handle_success(response)
            except:
                return self.handle_error(response)
        else:
            return self.handle_error(response)
