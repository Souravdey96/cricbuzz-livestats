import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Key": "625c4adec2mshb19d0c820f4c720p194f9ajsnc2c696b84eb7",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text[:500])