from requests import Session

link = "https://production-graphql.eu-sharedservices.olxcdn.com/graphql"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
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