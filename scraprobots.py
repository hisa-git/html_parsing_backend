import requests

def replace_after_third_slash(s: str, replacement: str) -> str:
    parts = s.split("/", 3)
    if len(parts) <= 3:
        return s + "/" + replacement
    else:
        return "/".join(parts[:3] + [replacement])
def scrap_robots(url: str) -> str:
    robots_url = replace_after_third_slash(url, "robots.txt")
    try:
        response = requests.get(robots_url, timeout=10)
    except requests.RequestException as e:
        return f"Ошибка при загрузке robots.txt: {e}"
    
    if response.status_code == 200:
        return response.text
    else:
        return "На сайте не найден robots.txt"
