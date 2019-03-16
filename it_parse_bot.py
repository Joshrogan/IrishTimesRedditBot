import praw, os, bs4, requests, time
from selenium import webdriver
from bs4 import BeautifulSoup

def main():
    start_time = time.time()
    reddit = login_reddit() 

    subreddit = reddit.subreddit("jrogan993Test")
    for submission in subreddit.stream.submissions():
        if submission.created_utc < start_time:
                continue
        if "irishtimes.com" in submission.url:
            browser = login_irishtimes()
            browser.get(submission.url)
            time.sleep(10)
            html = browser.page_source
            post_article(html, reddit, submission, browser)
            browser.quit()

def post_article(html, reddit, submission, browser):
    soup = BeautifulSoup(html, "lxml")
    article_para = soup.find_all('p', class_='no_name')
    article_text = ''

    for p in article_para:
        article_text += ('>' + p.get_text() + '\n\n')

    submission.reply(article_text)

def login_reddit():
    reddit = praw.Reddit(client_id = 'Ao4phq9377Rggg',
            client_secret = 'vfOop1WqPPz8nasr2HqstUXXa6E',
            username='coipeail', password='focalfaire',
            user_agent='itRepostBotAlpha')
    return reddit

def login_irishtimes():
    it_user = os.environ.get('IT_USER')
    it_password = os.environ.get('IT_PASS')
    driver = webdriver.Firefox()
    
    driver.get("https://www.irishtimes.com/signin")
    driver.find_element_by_id("email").send_keys(it_user)
    driver.find_element_by_id("password").send_keys(it_password)
    driver.find_element_by_class_name("it-btn").click()
    
    time.sleep(10)
    return driver

if __name__ == "__main__":
    main()
