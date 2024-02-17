import json

import requests

from apps.events.models import Event


class EventBriteService:
    def __init__(self):
        self.headers = self._get_headers()
        self.session = requests.Session()

    def _get_headers(self):
        return {
            'authority': 'www.eventbrite.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'cookie': 'mgrefby=; G=v%3D2%26i%3D27812d8d-ea28-4165-8520-06adac4dc465%26a%3D11ac%26s%3D99abab19c1ca45759b302dd663b5f8f16cd6f316; eblang=lo%3Den_US%26la%3Den-us; csrftoken=b03410a4570611eea5a41b7c100b7903; ebGAClientId=2076554435.1695139686; mgref=eafil; _hp2_props.1404198904=%7B%7D; _scid=ebfc3598-e647-4252-82df-72d6127ef866; _sctr=1%7C1695078000000; _tt_enable_cookie=1; _ttp=ZL1VA_j1DwveTYoFSpXAzXwKMU1; _pin_unauth=dWlkPVpXUmlOR0UzWXprdFltSmpNQzAwTWprekxXRTFPV1l0TTJJeVpEaGxaamhoTURZMQ; hubspotutk=e5457064597eebceb9e300eaf872d812; _scid_r=ebfc3598-e647-4252-82df-72d6127ef866; stableId=abed1d2f-301f-4630-b038-d442c58591eb; ebEventToTrack=; AN=; _gid=GA1.2.1064213614.1707867128; tinuiti=ec7839ec-3712-4759-8164-f04b8d5a4d53; _gcl_au=1.1.82108468.1707867128; _fbp=fb.1.1707867136100.720116377; SS=AE3DLHS2g19IFFr-5ynglCV8DW3Pu_WEBA; AS=02461022-71fa-4810-b0a4-daa1ca3fa099; __hstc=195498867.e5457064597eebceb9e300eaf872d812.1695139694344.1707867137206.1707867567585.3; __hssrc=1; ssr_experimentation_batch=False; mgaff779663934817=ebdssbcitybrowse; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%2211feebff-b9e2-4c70-96c8-7771db93cc78%22; mgaff779663934817=ebdssbcitybrowse; django_timezone=Africa/Lagos; mgaff799266978047=ehometext; mgaff799266978047=ehometext; _ga=GA1.1.2076554435.1695139686; _derived_epik=dj0yJnU9dFg3NW1pSHVGT1ZieXI1WmZlbFVqRy1tMC1YczhpYUQmbj1sYlFCdUlVTVpqYlBEZWtzbi16OG93Jm09MSZ0PUFBQUFBR1hNQS04JnJtPTEmcnQ9QUFBQUFHWE1BLTgmc3A9Mg; location={%22slug%22:%22nigeria--lagos%22%2C%22place_id%22:%22890437281%22%2C%22latitude%22:6.45306%2C%22longitude%22:3.39583%2C%22place_type%22:%22locality%22%2C%22current_place%22:%22Lagos%22%2C%22current_place_parent%22:%22Nigeria%22%2C%22is_using_current_location%22:false%2C%22is_online%22:false%2C%22user_lat_lng%22:null}; _gat=1; _ga_TQVES5V6SH=GS1.1.1707873249.3.0.1707873249.60.0.0; _hp2_ses_props.1404198904=%7B%22r%22%3A%22https%3A%2F%2Fwww.eventbrite.com%2Fb%2Fnigeria--akwa-lbom%2Fseasonal%2F%3Fbucket%3Dcelebrate-love%22%2C%22ts%22%3A1707873248732%2C%22d%22%3A%22www.eventbrite.com%22%2C%22h%22%3A%22%2Fd%2Fnigeria--lagos%2Fseminars%2F%22%2C%22q%22%3A%22%3Fpage%3D1%22%7D; SP=AGQgbbkWvcfaIzanQSuYmdWOxjKIuE8AZgme3ERIfZ6Lfq_2VUpgXkZuAJxWMzyZdD-BAX-Y9KZYVMIpbM7H9uddBsZKh04MAL2zKSgkun59btFTr_QxpMSErEcLZ566U4R2fpJWzZdckUtCYiNnlrztQqf3USBt5wZhn2ZDLrGAPnxH073hvcmfnnrmPsLQlxvndf2seljFT12_DXl34oN3jv0h2MTJKS1qBh10TmFeLIhqueItQwM; _dd_s=logs=1&id=982fbdb6-02cb-4f4c-ad6a-f7783f6f02b8&created=1707873248407&expire=1707874161802&rum=0; _hp2_id.1404198904=%7B%22userId%22%3A%22308167518066881%22%2C%22pageviewId%22%3A%227287885526310155%22%2C%22sessionId%22%3A%226003849727255420%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; AN=; AS=02461022-71fa-4810-b0a4-daa1ca3fa099; G=v%3D2%26i%3De1610685-af35-465e-b2ea-7c4cfcb48d69%26a%3D123f%26s%3D8ca1da50bd879a9cb0e2d7b9adbd878111b0cd11; SP=AGQgbbk4SSywM97DvcnPGCXShfLn7bDTPFCDF_Gjl5zNE-rRBBhV6yTD5F4c1M8TpaAHH9-UJ0STT1-cpD3_kLIppF1H4LHxgmQcYOJVs3EEZLuw6NOfQfd7vZq0agMG8WJxloYQ9xH7aXl9P4imMkOWpfq3_Ym-deOFDzwCge90fKN7D4Oa__24x7yPSoucZMtWPLM5y0Mn84txMJ3C1rtO61OM5ydtTp9ERJGBSPMw5JqMoR3XDbA; SS=AE3DLHQKgGjFErmvUSelnP2L1kKx_J5NtA; active_organization_id=1994087258753; ebEventToTrack=; eblang=lo%3Den_US%26la%3Den-us; stableId=abed1d2f-301f-4630-b038-d442c58591eb',
            'dnt': '1',
            'origin': 'https://www.eventbrite.com',
            'referer': 'https://www.eventbrite.com/d/nigeria--lagos/appearances/?page=1',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'x-csrftoken': 'b03410a4570611eea5a41b7c100b7903',
        }

    def get_events(self, states_ids: list):
        new_events = []
        events = self.__search_events(states_ids)
        events = self._filter_events(events)

        for event_info in events:
            if event := self._create_event(event_info):
                new_events.append(event)

        return new_events

    def __search_events(self, states_ids: list):
        all_events = []
        page_number = 1
        page_count = 1
        url = "https://www.eventbrite.com/api/v3/destination/search/"

        # Loop until all events on all pages are fetched
        while page_number <= page_count:
            payload = {
                "event_search": {
                    "dates": "current_future",
                    "dedup": True,
                    "places": states_ids,
                    "page": page_number,
                    "page_size": 100,
                    "online_events_only": False
                },
                "expand.destination_event": [
                    "primary_venue",
                    "image",
                ],
                "browse_surface": "search"
            }

            response = self.session.post(
                url=url,
                headers=self.headers,
                data=json.dumps(payload)
            )

            data = response.json()
            events = data.get('events', {}).get('results', [])
            all_events.extend(events)

            page_count = data['events']['pagination'].get('page_count', 0)
            page_number += 1

        return all_events

    def _filter_events(self, events):
        physical_events = filter(
            lambda event: not event.get("is_online_event"),
            events
        )

        return list(physical_events)

    def _create_event(self, event_info):
        event = Event.objects.filter(name=event_info["name"]).first()

        if not event:
            event = Event(
                name=event_info.get("name", ""),
                description=event_info.get("summary", ""),
                image=event_info.get("image", {}).get("url", ""),
                start_date=event_info.get("start_date", "2024-01-01"),
                end_date=event_info.get("end_date", "2024-01-01"),
                start_time=event_info.get("start_time", "00:01:01"),
                end_time=event_info.get("end_time", "00:01:01"),
                location=event_info["primary_venue"]["address"]["localized_address_display"],
            )
            event.save()

            return event
