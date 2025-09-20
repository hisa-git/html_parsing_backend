import requests

def replace_after_third_slash(s: str, replacement: str) -> str:
    parts = s.split("/", 3)
    if len(parts) <= 3:
        return s + "/" + replacement
    else:
        return "/".join(parts[:3] + [replacement])
def scrap_robots(url):
    robots_url = replace_after_third_slash(url,"robots.txt")
    response = requests.get(robots_url) 
    if response.status_code == 200: 
        print(response.text) 
        return response.content
    else: 
        print("No robots.txt file found.")
        return "На сайте не найден robots.txt"
    

