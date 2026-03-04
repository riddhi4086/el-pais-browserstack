from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://elpais.com")
time.sleep(3)
#Extracting Title of article
print("Website Title:", driver.title)

#Language Check
html_tag = driver.find_element(By.TAG_NAME, "html")
language = html_tag.get_attribute("lang")

print("Website Language:", language)

# Check condition
if language.startswith("es"):
    print("Website is in Spanish")
else:
    print("Website is NOT in Spanish")


#Opinion Page
opinion_url = "https://elpais.com/opinion/"
driver.get(opinion_url)
time.sleep(3)

# Confirmation print
print("Successfully navigated to Opinion section")

#Identifying articles on opinion page
articles = driver.find_elements(By.TAG_NAME, "article")

print(f"Total articles found on page: {len(articles)}") #total articles

first_five_articles = articles[:5]  #slicing  to 5 articles
print("First 5 articles selected")


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

article_titles_spanish = []
translator = Translator()
translated_titles = []  #for word analysis

for index in range(5):
    try:
        print(f"\n🔹 Processing article {index + 1}")

        articles = driver.find_elements(By.TAG_NAME, "article")
        article = articles[index]

        # Extracting Actual article link from headline
        headline_link = article.find_element(By.CSS_SELECTOR, "h2 a")
        article_url = headline_link.get_attribute("href")

        print("Opening URL:", article_url)
        driver.get(article_url)

        wait = WebDriverWait(driver, 10)

        # Presence check
        title_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.a_t"))
        )

        # Scrolling into view
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            title_element
        )

        title_text = title_element.text.strip()
        print("Spanish Title:", title_text)

        article_titles_spanish.append(title_text)

        # for translation
        try:
            translated = translator.translate(
                title_text,
                src='es',
                dest='en'
            )

            english_title = translated.text
            print("English Title:", english_title)

            translated_titles.append(english_title)     #appending to list

        except Exception as e:
            print("Translation failed:", e)


        # Performed Deduplication
        # Extracting Intro → Paragraphs → Figcaptions in content

        from selenium.common.exceptions import NoSuchElementException, TimeoutException
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        print("Article Content (Spanish):")

        content_parts = []
        seen_text = set()   #I've used set key to avoid duplication

        def add_text(text):
            text = text.strip()
            if text and text not in seen_text:
                seen_text.add(text)
                content_parts.append(text)

        #Intro
        try:
            standfirst = driver.find_element(By.CSS_SELECTOR, "h2.a_st")
            add_text(standfirst.text)
        except NoSuchElementException:
            pass

        #Paragraph-based content (deduplicated)
        content_selectors = [
            'div[data-dtm-region="articulo_cuerpo"]',
            'div.a_c',
            'section[itemprop="articleBody"]'
        ]

        for selector in content_selectors:
            try:
                container = driver.find_element(By.CSS_SELECTOR, selector)
                paragraphs = container.find_elements(By.TAG_NAME, "p")

                for p in paragraphs:
                    text = driver.execute_script(
                        "return arguments[0].textContent;", p
                    )
                    add_text(text)

            except NoSuchElementException:
                continue

        #Figcaption captions (deduplicated + added wait time)
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "figcaption.a_m_p span")
                )
            )

            captions = driver.find_elements(
                By.CSS_SELECTOR, "figcaption.a_m_p span"
            )

            for cap in captions:
                text = driver.execute_script(
                    "return arguments[0].textContent;", cap
                )
                add_text(text)

        except (NoSuchElementException, TimeoutException):
            pass

        #Final output
        if content_parts:
            article_content = "\n".join(content_parts)
            print(article_content)
        else:
            print("No readable text content found for this article")



        driver.get("https://elpais.com/opinion/")
        time.sleep(3)

    except Exception as e:
        print("Error while processing article:", e)
        driver.get("https://elpais.com/opinion/")
        time.sleep(3)


# Repeated words analysis from English titles
import re
from collections import Counter

# Common English stopwords
stopwords = {
    "the", "is", "in", "of", "and", "to", "a", "on", "for", "with",
    "as", "at", "by", "an", "from", "this", "that"
}

all_words = []

for title in translated_titles:
    # changing to Lowercase
    title = title.lower()

    # Remove punctuation (only letters and spaces)
    title = re.sub(r"[^a-z\s]", "", title)

    # Split into words
    words = title.split()

    for word in words:
        if word not in stopwords:
            all_words.append(word)

# Count frequency
word_counts = Counter(all_words)

print("\n Repeated words (appearing more than twice):")

found = False
for word, count in word_counts.items():
    if count > 2:
        print(f"{word} → {count}")  #Print words appearing more than 2 times
        found = True

if not found:
    print("No words repeated more than twice.")




