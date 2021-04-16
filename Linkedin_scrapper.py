#-----------libraries---------------------------------------------------
import random
from bs4 import BeautifulSoup as bs
import getpass
import re
import csv
from bs4 import BeautifulSoup,SoupStrainer
from selenium import webdriver
import time
import pandas as pd
#-----------------Selenium Chrome Webdriver-------------------------------
def setUp():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)
   

    #-------------------login-------------------------------------------------
    driver.get("https://www.linkedin.com/uas/login")
    time.sleep(2)

    emaile = driver.find_element_by_id("username")
    emaile.send_keys("")
    password = driver.find_element_by_id("password")
    password.send_keys("")

    #-----------------Connection Link-----------------------------------------
    url = driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
    total_height = driver.execute_script("return document.body.scrollHeight")
    i=0
    while i<=1:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.uniform(2.5, 4.9))
        # Calculate new scroll height and compare with total scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == total_height:
            break
        last_height = new_height
        i+=1

    page = bs(driver.page_source, features="html.parser")
    # # timee = page.select("div.mn-connection-card__details > time")
    content = page.find_all('a', {'class':"mn-connection-card__link ember-view"})

    timee=page.find_all('time', attrs={'class': 'time-badge time-ago'})
    tt=[]
    for t in timee:
        ti=t.text.replace('\n', " ")
        tt.append(ti.strip())

    mynetwork = []
    for contact in content:
        mynetwork.append(contact.get('href'))

    res = {}
    for key in mynetwork:
        for value in tt:
            res[key] = value
            tt.remove(value)
            break
    # print(res)
    c=[]
    for k,v in res.items():
        if v[10:15]=="2 day" or v[12:18]=="minute" or v[12:18]=="second" or v[12:16]=="hour":
            c.append(k)
        # if v[12:16]=="year":
        #     print("years")

    print(c)


    names = []
    links = []
    phones = []
    emails = []
    adressess = []
    companies = []
    countries = []
    position=[]
    birth=[]
    # -----------------------Get Connections Links-------------------------------------
    for contact in c:
        driver.get("https://www.linkedin.com" + contact)
        contact_page = bs(driver.page_source, features="html.parser")


        try:
            country = contact_page.select(
                "div.flex-1.mr5 > ul.pv-top-card--list.pv-top-card--list-bullet.mt1 > li.t-16.t-black.t-normal.inline-block")
            print(country)
            if len(country) == 0:
                country = "not found"
                countries.append(country.strip())
            else:
                for c in country:
                    cont = c.text.replace('\n', " ")
                    # print("link",profile)
                    countries.append(cont.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("link not found")

        try:
            pos = contact_page.select(
                "div.ph5.pb5 > div.display-flex.mt2 > div.flex-1.mr5 > h2")
            if len(pos) == 0:
                pos = "not found"
                position.append(pos.strip())
            else:
                for pp in pos:
                    cont = pp.text.replace('\n', " ")
                    # print("link",profile)
                    position.append(cont.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
                print("position not found")
        try:
            company = contact_page.find_all('ul',attrs= {'class': 'pv-top-card--experience-list'})
            if len(company) == 0:
                compan = "not found"
                companies.append(compan.strip())
            else:
                for cp in company:
                    compp = cp.text.replace('\n'," ")
                    # print("link",profile)
                    companies.append(compp.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("company not found")


        driver.get("https://www.linkedin.com" + contact + "detail/contact-info/")
        driver.implicitly_wait(3)
        contact_page = bs(driver.page_source, features="html.parser")
        # ----------------Scrape Profile Links-------------------------
        try:
            profileLink=contact_page.select("div > section.pv-contact-info__contact-type.ci-vanity-url > div > a")
            if len(profileLink)==0:
                profile="not found"
                links.append(profile.strip())
            else:
                for pl in profileLink:
                    profile = pl.text.replace('\n'," ")
                    # print("link",profile)
                    links.append(profile.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("link not found")
        # -----------------Scrape Name--------------------------------
        try:
            name = contact_page.find_all('h1', attrs={'id': 'pv-contact-info'})
            if len(name)==0:
                namee="not found"
                names.append(namee.strip())
            else:
                for n in name:
                    namee = n.text.replace('\n'," ")
                    # print("name",namee)
                    names.append(namee.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("name not found")

        # ---------------------------Scrape Email-----------------------------------
        try:
            email = contact_page.find_all('a', href=re.compile("mailto"))
            if len(email)==0:
                emaill="not found"
                emails.append(emaill.strip())
            else:
                for e in email:
                    emaill=e.text.replace('\n'," ")
                    # print("email",emaill)
                    emails.append(emaill.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("email not found")

        #---------------------------Bday---------
        try:
            bday = contact_page.select("div > section.pv-contact-info__contact-type.ci-birthday > div > span")
            if len(bday) == 0:
                b = "not found"
                birth.append(b.strip())
            else:
                for b in bday:
                    bb = b.text.replace('\n', " ")
                    # print("email",emaill)
                    birth.append(bb.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("bday not found")

        # -----------------------------Scrape Phone-------------------------------------
        try:
            phone = contact_page.find_all('span', attrs ={'class': 't-14 t-black t-normal'})

            if len(phone) ==0:
                phon="not found"
                phones.append(phon.strip())
            else:
                for ph in phone:
                    phon = ph.text.replace('\n'," ")
                    # print("Phone", phon)
                    phones.append(phon)
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print("phone not found")
        # -------------------------------Scrape Address----------------------------------
        try:
            address=contact_page.select("div > section.pv-contact-info__contact-type.ci-address > div > a")
            if len(address)==0:
               adrs="not found"
               adressess.append(adrs.strip())

            else:
                for ad in address:
                    adrs=ad.text.replace('\n'," ")
                    # print("Address",adrs)
                    adressess.append(adrs.strip())
                time.sleep(random.uniform(0.5, 1.9))
        except:
            print(" adress not found")

    # print(links)
    # print(names)
    # print(emails)
    # print(phones)
    # print(adressess)
    # print(countries)
    # print(position)
    # print(companies)
    # ----------------Store in Excel CSV---------------------
    data=[links,names,emails,phones,adressess,countries,position,companies,birth]
    df=pd.DataFrame(data, index=['Link','Name','Email','Phone','Address','City/ State/ Country','Position','Company','Birthday'])
    tdf=df.T
    tdf.to_csv('data21c1.csv')

    driver.quit()

setUp()

