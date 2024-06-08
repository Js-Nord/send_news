import requests
from twilio.rest import Client

STOCK_NAME = "WHATEVER_COMPANY"
account_sid = "YOUR_SID"
auth_token = "YOUR_TOKEN"
STOCK_ENDPOINT = "STOCK_API"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

response = requests.get("DESIRED_API_STOCK")
response.raise_for_status()
data = response.json()

close_list = [dict["close"] for dict in data]


def percentage_difference(a, b):
    diff = abs(a - b)
    avg = (a + b) / 2
    perc_diff = (diff / avg) * 100
    return perc_diff


percentage_diff = percentage_difference(close_list[0], close_list[1])
parameters = {
    "apiKey": "YOUR_KEY",
    "q": STOCK_NAME,
    "searchIN": "title",
    "from": "FROM_X(YY-MM-DD)",
    "to": "TO_X(YY-MM-DD)"
}
response_news = requests.get("https://newsapi.org/v2/everything", params=parameters)
response_news.raise_for_status()
data = response_news.json()
for articles in data["articles"]:
    news_list = data["articles"][1:]
    relevant = ["title", "description"]
    new_data = [{key: d[key] for key in relevant} for d in news_list]
    if percentage_diff > 5:
        client = Client(account_sid, auth_token)
        for i, article in enumerate(new_data[:3]):  # Send only up to 3 messages
            try:
                message_1 = client.messages.create(from_='TWILIO_NUMBER',
                                                   body=f'Headline: {new_data[0]["title"]}\n'
                                                        f'Brief: {new_data[0]["description"]}',
                                                   to='YOUR_NUMBER')
                message_2 = client.messages.create(from_='TWILIO_NUMBER',
                                                   body=f'Headline: {new_data[1]["title"]}\n'
                                                        f'Brief: {new_data[1]["description"]}',
                                                   to='YOUR_NUMBER')
                message_3 = client.messages.create(from_='TWILIO_NUMBER',
                                                   body=f'Headline: {new_data[2]["title"]}\n'
                                                        f'Brief: {new_data[2]["description"]}',
                                                   to='YOUR_NUMBER')
            except Exception:
                print("Message not sent")

