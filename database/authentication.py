import requests
session = requests.session()

url = 'https://users.premierleague.com/accounts/login/'
payload = {
 'password': 'FPLpassword123!',
 'login': 'pete.j.matt@gmail.com',
 'redirect_uri': 'https://fantasy.premierleague.com/a/login',
 'app': 'plfpl-web'
}
session.post(url, data=payload)