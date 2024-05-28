import json
from requests import Session

link = "https://production-graphql.eu-sharedservices.olxcdn.com/graphql"

headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "apollo-require-preflight": "true",
}


def main(link):
    s = Session()
    s.headers.update(headers)

    query = {
        "query": """
        query {
          myAds {
            pageViews {
              pageViews
              __typename
            }
            __typename
          }
        }
        """
    }

    response = s.post(link, json=query)

    if response.status_code == 200:
        data = response.json()
        # Extract the number of page views
        page_views = data.get("data", {}).get("myAds", {}).get("pageViews", {}).get("pageViews", None)

        print(f"Page Views: {page_views}")

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print(f"Query failed to run with status code {response.status_code}")
        print(f"Response: {response.text}")


main(link)

"""
from requests import Session

link = "https://production-graphql.eu-sharedservices.olxcdn.com/graphql"

headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "apollo-require-preflight": "true",
}

def main(link):
    s = Session()
    s.headers.update(headers)

    response = s.get(link)
    with open('data.html', 'w', encoding='utf-8') as r:
        r.write(response.text)


main(link)
"""