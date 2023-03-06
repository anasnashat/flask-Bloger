import requests
ip_list = []
# get my ip address
ip = requests.get('https://api.ipify.org').text
if ip not in ip_list:
    ip_list.append(ip)
views = len(ip_list)
requests.get(f'https://api.telegram.org/bot5964632324:AAHCoXpLJNEUjdNLAMicqDpkOcNWAFjwfZk/sendMessage?chat_id=731370645&text=number of views: {views}')


