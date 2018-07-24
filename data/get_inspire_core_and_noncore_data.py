'''
This snippet is supposed to be run from within the inspirehep shell.
'''

from invenio_search import current_search_client as es
from elasticsearch.helpers import scan
from inspire_utils.record import get_value

core_records = []
noncore_records = []

query = {
            "query":
            {
                    "bool":
                    {
                        "must":
                        [
                            {
                                "exists":
                                {
                                    "field": "earliest_date"
                                }
                            },
                            {
                                "exists":
                                {
                                    "field": "titles"
                                }
                            },
                            {
                                "exists":
                                {
                                    "field": "abstracts"
                                }
                            },
                            {
                                "range":
                                {
                                    "earliest_date":
                                    {
                                        "gte": "2016-01-01",
                                        "format": "yyyy||yyyy-MM||yyyy-MM-dd"
                                    }
                                }
                            }
                        ]
                    }
            },
            "_source":
            [
                "earliest_date",
                "control_number",
                "core",
                "titles.title",
                "abstracts.value"
            ]
        }

for hit in scan(es, query=query, index='records-hep', doc_type='hep'):
    coreness = get_value(hit, '_source.core')
    if coreness is True:
        core_records.append(hit['_source'])
    else:
        noncore_records.append(hit['_source'])
