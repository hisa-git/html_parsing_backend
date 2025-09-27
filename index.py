from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import time
from htmltags import HTML_TAGS
from wordsanalyze import analyze_text_content
from scraprobots import scrap_robots
from scrapsitemap import get_sitemap
import re

app = FastAPI(title="SEO Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://html-reader-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "SEO Analyzer API работает!", "status": "online"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/analyze")
def analyze_url(request: UrlRequest):
    """Анализ веб-страницы по URL"""
    try:
        print(f"🔍 Анализируем URL: {request.url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        start_time = time.time()
        response = requests.get(request.url, headers=headers, timeout=15)
        load_time = time.time() - start_time
        
        print(f"📡 HTTP Status: {response.status_code}")
        print(f"📡 Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"📡 Content-Encoding: {response.headers.get('content-encoding', 'none')}")
        print(f"📡 Response size: {len(response.content)} bytes")
        
        if response.status_code != 200:
            return {"error": f"Ошибка загрузки: {response.status_code}"}
        
        encoding = response.encoding or 'utf-8'
        
        if encoding == 'ISO-8859-1':
            content_preview = response.content[:2000].decode('utf-8', errors='ignore')
            charset_match = re.search(r'charset[=:]\s*([-\w.]+)', content_preview, re.IGNORECASE)
            if charset_match:
                encoding = charset_match.group(1)
                print(f"📡 Найдена кодировка в HTML: {encoding}")
            else:
                encoding = 'utf-8'
        
        print(f"📡 Используем кодировку: {encoding}")
        
        try:
            html_content = response.content.decode(encoding, errors='replace')
        except (UnicodeDecodeError, LookupError):
            html_content = response.content.decode('utf-8', errors='replace')
        
        print(f"📄 HTML preview: {html_content[:200]}...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title_tag = soup.find('title')
        title_text = title_tag.get_text().strip() if title_tag else "Заголовок не найден"
        
        meta_description = soup.find('meta', attrs={'name': 'description'}) or \
                          soup.find('meta', attrs={'property': 'og:description'}) or \
                          soup.find('meta', attrs={'name': 'Description'})
        
        description = meta_description.get('content', '').strip() if meta_description else "Описание не найдено"
        
        print(f"📝 Title найден: {title_text[:100]}...")
        print(f"📝 Description найден: {description[:100]}...")
        
        tag_counts = {}
        important_tags = HTML_TAGS
        
        for tag in important_tags:
            count = len(soup.find_all(tag))
            tag_counts[tag] = count
            if count > 0:
                print(f"🏷️  {tag.upper()} тегов: {count}")
        
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt') or not img.get('alt').strip()]
        
        print(f"Изображений всего: {len(images)}, без alt: {len(images_without_alt)}")
        
        content_analysis = analyze_text_content(soup)
        
        print(f"Найдено ключевых слов: {len(content_analysis['keyword_density'])}")
        
        og_title = soup.find('meta', property='og:title')
        og_description = soup.find('meta', property='og:description')
        og_image = soup.find('meta', property='og:image')
        
        canonical = soup.find('link', rel='canonical')
        robots_content = scrap_robots(request.url)
        sitemap = get_sitemap(request.url)
        
        return {
            "url": request.url,
            "status": "success",
            "basic_info": {
                "title": title_text,
                "title_length": len(title_text),
                "description": description,
                "description_length": len(description),
                "og_title": og_title.get('content', '') if og_title else '',
                "og_description": og_description.get('content', '') if og_description else '',
                "og_image": og_image.get('content', '') if og_image else '',
                "canonical": canonical.get('href', '') if canonical else ''
            },
            "structure": {
                "tag_counts": tag_counts,
                "total_images": len(images),
                "images_without_alt": len(images_without_alt),
                "heading_structure": {
                    "h1_texts": [h.get_text().strip()[:100] for h in soup.find_all('h1')],
                    "h2_texts": [h.get_text().strip()[:100] for h in soup.find_all('h2')][:5]
                }
            },
            "content": {
                "word_count": content_analysis['word_count'],
                "char_count": content_analysis['char_count'],
                "unique_words": content_analysis['unique_words'],
                "language": content_analysis['language'],
                "keyword_density": content_analysis['keyword_density']
            },
            "technical": {
                "load_time_seconds": round(load_time, 2),
                "page_size_bytes": len(response.content),
                "status_code": response.status_code,
                "content_encoding": response.headers.get('content-encoding', ''),
                "server": response.headers.get('server', ''),
                "detected_encoding": encoding,
                "robots": robots_content,
                "sitemap": sitemap
            }
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Timeout: сайт слишком долго отвечает"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection Error: не удается подключиться к сайту"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка запроса: {str(e)}"}
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Ошибка парсинга: {str(e)}"}
    
    
if __name__ == "__main__":
    import uvicorn
    print("Запуск SEO Analyzer API сервера...")
    print("Сервер будет доступен по адресу: http://localhost:8000")
    print("Документация API: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)