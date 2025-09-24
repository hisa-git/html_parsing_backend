from scraprobots import scrap_robots
from scraprobots import replace_after_third_slash
import requests

def parse_robots_for_sitemap(robots_content):
    sitemaps = []
    for line in robots_content.split('\n'):
        if line.strip().lower().startswith('sitemap:'):
            sitemap_url = line.split(':', 1)[1].strip()
            sitemaps.append(sitemap_url)
    return sitemaps

def get_sitemap(url):
    robots_content = scrap_robots(url)
    if robots_content and robots_content != "No robots.txt file found":
        sitemaps = parse_robots_for_sitemap(robots_content)
        if sitemaps:
            response = requests.get(sitemaps[0])
            if response.status_code == 200:
                return response.text
    
    base_url = replace_after_third_slash(url, "")
    standard_paths = ['sitemap.xml', 'sitemap_index.xml', 'sitemaps.xml']
    
    for path in standard_paths:
        sitemap_url = base_url + path
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            return response.text
    
    return "Sitemap не найден"