from instagram import InstagramAPI

CONFIG = {
  'client_id': 'd67c76fb37a541efbb77d0a5a294bcf8',
  'client_secret': 'e6c4c8a1ae344f0aaa261593b116fc8a',
  'redirect_uri': 'http://localhost:8515/oauth_callback',
  'geo_lat': -122.2744,
  'geo_long': 37.87095
}

api = InstagramAPI(client_id = CONFIG['client_id'], client_secret = CONFIG['client_secret'])
berkeley = api.create_subscription(object='geography', lat=CONFIG['geo_lat'], lng=CONFIG['geo_long'], radius=1000, aspect='media', callback_url='http://mydomain.com/hook/instagram')

reactor = subscriptions.SubscriptionsReactor()
