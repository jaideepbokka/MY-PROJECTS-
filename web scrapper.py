"""
Single-file Book Price Comparator (Demo Skeleton)

NOTE:
Major e-commerce sites frequently change their HTML and use anti-bot
protections. This example uses Selenium and is intended as a learning
project. You may need to update CSS selectors over time.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

def start_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1400,1000")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def search_amazon(driver, book):
    try:
        url=f"https://www.amazon.in/s?k={book.replace(' ','+')}"
        driver.get(url)
        time.sleep(3)
        title=driver.find_element(By.CSS_SELECTOR,"h2 span").text
        price=driver.find_element(By.CSS_SELECTOR,"span.a-price-whole").text
        return {"Website":"Amazon","Title":title,"Price":int(price.replace(",",""))}
    except Exception:
        return None

def search_flipkart(driver, book):
    try:
        url=f"https://www.flipkart.com/search?q={book.replace(' ','+')}"
        driver.get(url)
        time.sleep(3)
        title=driver.find_element(By.CSS_SELECTOR,"div.KzDlHZ").text
        price=driver.find_element(By.CSS_SELECTOR,"div.Nx9bqj").text
        digits="".join(c for c in price if c.isdigit())
        return {"Website":"Flipkart","Title":title,"Price":int(digits)}
    except Exception:
        return None

def main():
    book=input("Enter book name: ")
    driver=start_driver()
    results=[]
    for fn in (search_amazon,search_flipkart):
        r=fn(driver,book)
        if r:
            results.append(r)
    driver.quit()
    if not results:
        print("No results found.")
        return
    df=pd.DataFrame(results).sort_values("Price")
    print("\nPrice Comparison\n")
    print(df.to_string(index=False))
    best=df.iloc[0]
    print(f"\nBest Deal: {best['Website']} - ₹{best['Price']}")
    df.to_csv("price_report.csv",index=False)
    print("Saved as price_report.csv")

if __name__=="__main__":
    main()
