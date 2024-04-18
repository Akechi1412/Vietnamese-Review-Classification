from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import time
import csv

def save_to_csv(review_list):
    with open('data/reviews_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(review_list)

class TikiReviewCrawler:
    def __init__(self, num_categories=10, num_products=10, review_pages=10):
        chrome_options = Options()  
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.num_categories = num_categories
        self.num_products = num_products
        self.review_pages = review_pages
        self.review_filter_five = None
        self.review_filter_four = None
        self.review_filter_three = None
        self.review_filter_two = None
        self.review_filter_one = None

    def __del__(self):
        self.driver.quit()

    def scroll_to_load(self):
        SCROLL_PAUSE_TIME = 0.2
        SCROLL_LENGTH = 200

        last_height = self.driver.execute_script("return window.pageYOffset")

        while True:
            self.driver.execute_script(f"window.scrollBy(0, {SCROLL_LENGTH})")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return window.pageYOffset")
            if new_height == last_height:
                break
            last_height = new_height

    def get_reviews(self, type):
        reviews = []
        i = 0
        while i < self.review_pages:
            try:
                review_elements = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.review-comment__content')
                ))
                for element in review_elements:
                    review = ''
                    try:
                        show_more_button = element.find_element(By.CSS_SELECTOR, 'div span.show-more-content')
                        self.driver.execute_script('arguments[0].click()', show_more_button)
                        review = element.find_element(By.CSS_SELECTOR, 'div span').text
                    except NoSuchElementException:
                        review = element.text

                    review.replace('(*) Đánh giá không tính điểm', '')
                    if review != '' or review.strip():
                        reviews.append([review, type])
                
                print(f'Done page {i + 1}')

                next_button = self.driver.find_element(By.CSS_SELECTOR, 'a.btn.next')
                is_disable_button = next_button.find_element(By.TAG_NAME, 'svg').get_attribute('color') == '#C4C4CF'
                if is_disable_button:
                    break
                else:
                    self.driver.execute_script("arguments[0].click()", next_button)
                    time.sleep(2)
                    i += 1
            except NoSuchElementException:
                if type == 0:
                    print("No positvie reviews!")
                elif type == 1:
                    print("No negative reviews!")
                elif type == 2:
                    print("No neutral reviews!")
                break
            except (TimeoutException, WebDriverException) as err:
                print(err)
                break

        return reviews

    def get_postive_reviews(self):
        print("Crawling positive reviews...")
        self.driver.execute_script('arguments[0].click()', self.review_filter_five)
        self.driver.execute_script('arguments[0].click()', self.review_filter_four)
        time.sleep(2)

        postitive_reviews = self.get_reviews(type=0)
        
        self.driver.execute_script('arguments[0].click()', self.review_filter_five)
        self.driver.execute_script('arguments[0].click()', self.review_filter_four)

        return postitive_reviews

    def get_negative_reviews(self):
        print("Crawling nagative reviews...")
        self.driver.execute_script('arguments[0].click()', self.review_filter_one)
        self.driver.execute_script('arguments[0].click()', self.review_filter_two)
        time.sleep(2)

        negative_reviews = self.get_reviews(type=1)
        
        self.driver.execute_script('arguments[0].click()', self.review_filter_one)
        self.driver.execute_script('arguments[0].click()', self.review_filter_two)

        return negative_reviews
    
    def get_neutral_reviews(self):
        print("Crawling neutral reviews...")
        self.driver.execute_script('arguments[0].click()', self.review_filter_three)
        time.sleep(2)

        neutral_reviews = self.get_reviews(type=2)
        
        self.driver.execute_script('arguments[0].click()', self.review_filter_three)

        return neutral_reviews

    def get_review_list_from_product(self, url):
        self.driver.get(url=url)
        print(f'Crawling data in product: {self.driver.title}...')
        self.scroll_to_load()

        try:
            self.review_filter_five = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'filter-review__item') and contains(., '5')]")
            ))
            self.review_filter_four = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'filter-review__item') and contains(., '4')]")
            ))
            self.review_filter_three = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'filter-review__item') and contains(., '3')]")
            ))
            self.review_filter_two = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'filter-review__item') and contains(., '2')]")
            ))
            self.review_filter_one = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'filter-review__item') and contains(., '1')]")
            ))

            positive_reviews = self.get_postive_reviews()
            negative_reviews = self.get_negative_reviews()
            neutral_reviews = self.get_neutral_reviews()
            review_list = positive_reviews + negative_reviews + neutral_reviews
            return review_list

        except:
            print('No review filters!')
            return []

    def get_review_list_from_category(self, url):
        self.driver.get(url=url)
        print(f'Crawling data in category: {self.driver.title}...')
        self.scroll_to_load()

        try:
            product_links = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.product-item')
            ))

            product_hrefs = [link.get_attribute('href') for link in product_links]
            product_hrefs = product_hrefs[:self.num_products]
            review_list = []
            for href in product_hrefs:
                review_list += self.get_review_list_from_product(url=href)
            return review_list
        except:
            print('No products!')
            return []

    def get_review_list(self, url):
        self.driver.get(url=url)
        categories = None
        try:
            categories = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR,'div.styles__StyledListItem-sc-w7gnxl-0.cjqkgR')
            ))
            category_hrefs = [link.get_attribute('href') 
                              for link in categories.find_elements(By.CSS_SELECTOR, 'div > a')]
            category_hrefs = category_hrefs[:self.num_categories]
            review_list = []
            for href in category_hrefs:
                review_list += self.get_review_list_from_category(url=href)
            return review_list
        except:
            print('No categories!')
            return []

if __name__ == '__main__':
    """
        num_categories: Number of categories in home page
        num_products: Number of products in each category page
        review_pages: Number of review pages in each product page
    """
    review_crawler = TikiReviewCrawler(num_categories=21, num_products=10, review_pages=10)
    url = 'https://tiki.vn/'
    review_list = review_crawler.get_review_list(url=url)
    save_to_csv(review_list)