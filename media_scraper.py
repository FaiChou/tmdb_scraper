from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

class MediaScraper:
    def __init__(self, media_type='movie'):
        # media_type 可以是 'movie' 或 'tv'
        self.media_type = media_type
        self.driver = webdriver.Chrome()
        self.items = []
        # 根据媒体类型设置不同的目标数量
        self.target_count = 250 if media_type == 'movie' else 150
        
    def get_media_links(self):
        # 尝试从文件加载已保存的链接
        links_file = f'{self.media_type}_links.json'
        try:
            with open(links_file, 'r', encoding='utf-8') as f:
                saved_links = json.load(f)
                if len(saved_links) >= self.target_count:
                    print(f"从文件加载了 {len(saved_links)} 个{self.media_type}链接")
                    return saved_links[:self.target_count]
        except FileNotFoundError:
            print(f"未找到已保存的{self.media_type}链接文件，开始重新爬取")
        
        # 访问主页开始爬取
        base_url = f'https://www.themoviedb.org/{self.media_type}/top-rated'
        self.driver.get(base_url)
        
        # 处理 cookie banner
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
        except Exception as e:
            print(f"处理 cookie banner 时出错: {str(e)}")
        
        media_links = []
        
        # 点击第一次 load more
        try:
            load_more = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#pagination_page_1 p.load_more a'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", load_more)
            load_more.click()
            time.sleep(2)
        except Exception as e:
            print(f"点击 Load More 时出错: {str(e)}")
        
        while len(media_links) < self.target_count:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.page_wrapper div.card a')
            current_links = [elem.get_attribute('href') for elem in elements]
            media_links = list(dict.fromkeys(current_links))
            
            print(f"当前已获取 {len(media_links)} 个{self.media_type}链接")
            
            if len(media_links) >= self.target_count:
                with open(links_file, 'w', encoding='utf-8') as f:
                    json.dump(media_links[:self.target_count], f, ensure_ascii=False, indent=2)
                break
        
        return media_links[:self.target_count]
    
    def scrape_media_details(self, url):
        self.driver.get(url)
        time.sleep(2)
        
        try:
            # 获取标题
            title = self.driver.find_element(By.CSS_SELECTOR, 'div.title h2 a').text.strip()
            
            # 获取简介
            overview = self.driver.find_element(By.CSS_SELECTOR, 'div.overview p').text.strip()
            
            # 获取演员表
            cast_elements = self.driver.find_elements(By.CSS_SELECTOR, 'li.card')[:10]
            cast = []
            for element in cast_elements:
                character = element.find_element(By.CSS_SELECTOR, 'p.character').text.strip()
                cast.append(character)
            
            return {
                'title': title,
                'overview': overview,
                'cast': cast
            }
        except Exception as e:
            print(f"获取{self.media_type}详情时出错: {str(e)}")
            return None
    
    def run(self):
        try:
            media_links = self.get_media_links()
            print(f"找到 {len(media_links)} 个{self.media_type}链接")
            
            # 尝试从文件加载已爬取的数据
            data_file = f'{self.media_type}s.json'
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.items = json.load(f)
                    print(f"从文件加载了 {len(self.items)} 个{self.media_type}数据")
            except FileNotFoundError:
                self.items = []
            
            # 获取已爬取的链接集合
            scraped_links = {item.get('url', '') for item in self.items}
            
            # 遍历未爬取的链接获取详情
            for i, link in enumerate(media_links, 1):
                if link in scraped_links:
                    print(f"跳过已爬取的{self.media_type}: {link}")
                    continue
                
                print(f"正在处理第 {i} 个{self.media_type}: {link}")
                media_data = self.scrape_media_details(link)
                if media_data:
                    media_data['url'] = link
                    self.items.append(media_data)
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(self.items, f, ensure_ascii=False, indent=2)
                
        finally:
            self.driver.quit()

if __name__ == "__main__":
    # 爬取电影
    # movie_scraper = MediaScraper(media_type='movie')
    # movie_scraper.run()
    
    # 爬取电视剧
    tv_scraper = MediaScraper(media_type='tv')
    tv_scraper.run()
