from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


client = MongoClient('127.0.0.1', 27017)
db = client['db']
mails_db = db.mails

chrome_options = Options()
chrome_options.add_argument('start-maximized')
s = Service('./chromedriver.exe')
drv = webdriver.Chrome(service=s, options=chrome_options)
drv.get("https://account.mail.ru/")
drv.implicitly_wait(30)


input_user = WebDriverWait(drv, 5).until(
    EC.presence_of_element_located((By.NAME, 'username')))
input_user.send_keys('study.ai_172@mail.ru')
input_user.send_keys(Keys.ENTER)

input_password = WebDriverWait(drv, 5).until(
    EC.element_to_be_clickable((By.NAME, 'password')))
input_password.send_keys('NextPassword172#')
input_password.send_keys(Keys.ENTER)

mail_count_elem = WebDriverWait(drv, 5).until(
    EC.presence_of_element_located((By.XPATH, "//nav/a[contains(@class, 'js-shortcut')][1]")))
mail_count = int(mail_count_elem.get_attribute('title').split()[1])
mail_link_set = set()
last_mail = None

while len(mail_link_set) < mail_count:
    mails = WebDriverWait(drv, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'js-letter-list-item')]")))
    mails_link = [mail.get_attribute('href') for mail in mails]
    mail_link_set = mail_link_set.union(set(mails_link))
    actions = ActionChains(drv)
    actions.move_to_element(mails[-1])
    actions.perform()

print(len(mail_link_set))

mails_info = []
for link in mail_link_set:
    if isinstance(link, str):
        mail_info = {}
        drv.get(link)
        source = WebDriverWait(drv, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact')))
        author = source.find_element(By.XPATH, "//span[1][@class='letter-contact']")
        mail_info['author'] = author.text
        date = source.find_element(By.XPATH, "//div[@class='letter__date']")
        mail_info['date'] = date.text
        subject = source.find_element(By.XPATH, "//h2[@class='thread-subject']")
        mail_info['subject'] = subject.text
        text = source.find_element(By.XPATH, "//div[@class='letter__body']")
        mail_info['text'] = text.text
        mails_info.append(mail_info)

mails_db.insert_many(mails_info)
print(f'Number of mails: {mails_db.count_documents({})}')
