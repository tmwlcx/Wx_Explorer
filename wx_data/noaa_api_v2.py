# NOAA API V2
# Documentation can be found at
# http://www.ncdc.noaa.gov/cdo-web/webservices/v2

# Credit @ crvaden https://github.com/crvaden/NOAA_API_v2/blob/Update/noaa_api_v2.py


import requests


class NOAAData(object):
    def __init__(self, token):
        # NOAA API Endpoint
        self.url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'
        self.h = dict(token=token)
        # self.p = None

    def poll_api(self, req_type, payload, limit=1000):
        # Initiate http request - kwargs are constructed into a dict and passed as optional parameters
        # Ex (limit=100, sortorder='desc', startdate='1970-10-03', etc)
        payload['limit']= limit
        r = requests.get(self.url + req_type, headers=self.h, params=payload)  
        print(f"fetching {r.request.url}")
        # print(f"with headers {r.request.headers}")      
        if r.status_code != 200:  # Handle erroneous requests
            print("Error: " + str(r.status_code))
            print(f"more information: \n{r.text}")
        else:
            r = r.json()
            # print(r)
            # print(r.keys())
            print(f"Metadata for {req_type}: \n {r['metadata']}")
            if 'metadata' in r.keys():
                _offset = r['metadata']['resultset']['offset']
                _count = r['metadata']['resultset']['count']
                while _offset + limit <= _count:
                    payload['offset'] = _offset + limit
                    r_add = requests.get(self.url + req_type, headers=self.h, params=payload) 
                    r_add = r_add.json()
                    r['results'].extend(r_add['results'])
                    _offset += limit

            try:
                return r['results']  # Most JSON results are nested under 'results' key
            except KeyError:
                return r  # for non-nested results, return the entire JSON string

    # Fetch available datasets
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#datasets
    def datasets(self, **kwargs):
        req_type = 'datasets'
        return self.poll_api(req_type, kwargs)

    # Fetch data categories
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#dataCategories
    def data_categories(self, **kwargs):
        req_type = 'datacategories'
        return self.poll_api(req_type, kwargs)

    # Fetch data types
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#dataTypes
    def data_types(self, **kwargs):
        req_type = 'datatypes'
        return self.poll_api(req_type, kwargs)

    # Fetch available location categories
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#locationCategories
    def location_categories(self, **kwargs):
        req_type = 'locationcategories'
        return self.poll_api(req_type, kwargs)

    # Fetch all available locations
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#locations
    def locations(self, **kwargs):
        req_type = 'locations'
        return self.poll_api(req_type, kwargs)

    # Fetch All available stations
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#stations
    def stations(self, h=None, p=None, **kwargs):
        req_type = 'stations'
        return self.poll_api(req_type, kwargs)

    # Fetch All data for specific station
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#stations
    def station_spec(self, stationid, **kwargs):
        req_type = 'stations/' + stationid
        return self.poll_api(req_type, kwargs)


    # Fetch information about specific dataset
    def dataset_spec(self, set_code, **kwargs):
        req_type = 'datacategories/' + set_code
        return self.poll_api(req_type, kwargs)

    # Fetch data
    # http://www.ncdc.noaa.gov/cdo-web/webservices/v2#data
    def fetch_data(self, **kwargs):
        req_type = 'data'
        return self.poll_api(req_type, kwargs)