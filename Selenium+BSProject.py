from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

def civil():
    url = 'https://civil.ge/archives/category/news'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    content = soup.find('div', class_ = 'mag-box-container clearfix')
    articles = content.find_all('li', class_ = 'post-item')
    time = 0
    civilcontent(content, articles, time, url)  

def timecivil(cfromdate, ctodate):
    url = 'https://civil.ge/archive?post_date=' + cfromdate + '+' + ctodate
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    content = soup.find('div', class_ = 'search-filter-results')
    articles = content.find_all('div', style = 'border-bottom: dashed 1px #ccc;')
    time = 1
    civilcontent(content, articles, time, url) 

def civilcontent(content, articles, time, url):
    pages, flag = 0, 0
    while flag == 0:
        ddates = content.find_all('span', class_ = 'fa fa-clock-o')
        dlinks = content.find_all('a', rel = 'category tag')
        for ddate in ddates:
            ddate.decompose()
        for dlink in dlinks:
            dlink.decompose()
        if time == 1:
            try:
                pages = content.find('ul', class_ = 'pages-numbers').find_all('li')
                current = content.find('li', class_ = 'current').span.text
                if (current == '1' or (current == str(len(pages) - 1))):
                    print('\nPage ' + current + ' of ' + str(len(pages) - 1))
                else:
                    print('\nPage ' + current + ' of ' + str(len(pages) - 2))
            except:
                print('\nPage 1 of 1')    
                flag = 1
        print('\nFound ' + str(len(articles)) + ' results in this page\n')

        for article in articles:
            date = article.span.span
            fnlink = article.find('a')
            print(date.text + ' -- ' ,fnlink.text)
            print(fnlink['href'], '\n')
            print('----------------------------------------------\n') 
        if flag == 1:
            break
        if time == 1:
            if current == str(len(pages) - 1):
                break
        flag = int(input('Input 0 to see more results or input 1 to view an article: '))
        if flag == 0:
            if time == 1:
                try:
                    url = url + '&sf_paged=' + str(int(current) + 1)
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'lxml')
                    content = soup.find('div', class_ = 'search-filter-results')
                    articles = content.find_all('div', style = 'border-bottom: dashed 1px #ccc;')
                except:
                    print('Failed to retrieve more results.')
                    flag = 1
            elif time == 0:
                morecivil(url, flag)
                flag = 1

def morecivil(url, flag):
    bot = webdriver.Firefox()
    bot.get(url)
    k = 1
    while flag == 0:           
        try:
            if k == 1:
                bot.execute_script('window.scrollTo(0, window.scrollY + 1400)')
                time.sleep(3)
            elif k > 1:
                bot.maximize_window()
                bot.execute_script("document.getElementById('load-more-archives').scrollIntoView();")
                time.sleep(2)
                bot.execute_script('window.scrollTo(0, 50)')
                time.sleep(2)
            bot.minimize_window()
            k += 1
        except:
            print('Failed to retrieve more results.')
            bot.quit()
            break
        page = bot.page_source
        soup = BeautifulSoup(page, 'lxml')
        content = soup.find('ul', class_ = 'posts-items')
        articles = content.find_all('li', class_ = 'posts-items-' + str(k)) 
        ddates = content.find_all('span', class_ = 'fa fa-clock-o')
        dlinks = content.find_all('a', rel = 'category tag')
        for ddate in ddates:
            ddate.decompose()
        for dlink in dlinks:
            dlink.decompose()  
        print('\nFound ' + str(len(articles)) + ' results in this page\n')
        for article in articles:
            date = article.span.span
            fnlink = article.find('a')
            print(date.text + ' -- ' ,fnlink.text)
            print(fnlink['href'], '\n')
            print('----------------------------------------------\n')
        flag = int(input('Input 0 to see more results or input 1 to view an article: '))

def civilarticle(wurl):
    article = requests.get(wurl)
    soup = BeautifulSoup(article.content, 'lxml')    
    title = soup.find('h1', class_ = 'post-title entry-title')   
    ddate = soup.find('span', class_ = 'fa fa-clock-o')        
    ddate.decompose()
    framedate = soup.find('div', class_ = 'post-meta')
    date = framedate.span
    body = soup.find('div', class_ = 'entry-content entry clearfix')
    paras = body.find_all('p')
    print('\n', date.text + ' -- ' + title.text, '\n')
    for para in paras:
        print(para.text, '\n')

def agenda():
    bot = webdriver.Firefox()
    aurl = 'https://agenda.ge/en/news/politics'
    bot.get(aurl)
    agendacontent(bot)
   
def timeagenda(y, m):
    bot = webdriver.Firefox()
    taurl = 'https://agenda.ge/en/news/news'  
    bot.get(taurl)
    page = bot.page_source  
    soup = BeautifulSoup(page, 'lxml')
    yearli = soup.find('li', class_ = 'select-year dropdown navbar-right selector')
    ylis = yearli.find_all('li')    
    i = 0
    for yli in ylis:
        ya = yli.find('a')
        i += 1
        if ya.text == y:
            bot.find_element_by_xpath('//*[@id="all-section"]/div/ul/li[4]/a').click()
            bot.find_element_by_xpath('//*[@id="all-section"]/div/ul/li[4]/ul/li[' + str(i) + ']/a').click()
            break
    monthli = soup.find('li', class_ = 'select-month dropdown navbar-right selector')
    mlis = monthli.find_all('li')
    k = 0
    for mli in mlis:
        ma = mli.find('a')
        k += 1    
        if ma.text == m:
            bot.find_element_by_xpath('//*[@id="all-section"]/div/ul/li[3]/a').click()
            bot.find_element_by_xpath('//*[@id="all-section"]/div/ul/li[3]/ul/li[' + str(k) + ']/a').click()
            break
    time.sleep(1)
    agendacontent(bot)

def agendacontent(bot):
    page = bot.page_source
    bot.minimize_window()
    flag = 0
    while flag == 0:
        soup = BeautifulSoup(page, 'lxml')
        content = soup.find('div', class_ = 'tab-pane active teasers-list')
        articles = content.find_all('div', class_ = 'col-md-3')
        print('\nFound ' + str(len(articles)) + ' results\n')
        for article in articles:
            date = article.find('div', class_ = 'node-teaser-time')
            alink = article.find('a', class_ = 'node-teaser-title')
            fnlink = 'https://agenda.ge' + alink['href']     
            print(date.text + ' -- ' + alink.text.strip())
            print(fnlink, '\n')
            print('----------------------------------------------\n')
        flag = int(input('Input 0 to see more results or input 1 to view an article: '))        
        if flag == 0:
            try:
                ataglis = soup.find('ul', class_ = 'pagination pagination-md navbar-right')
                alis = ataglis.find_all('li')
                bot.find_element_by_xpath('//*[@id="all-tab-content"]/div[5]/div/ul/li[' + str(len(alis)) + ']/a').click()  
                time.sleep(1)
                page = bot.page_source
            except:
                print('Failed to retrieve more results.')
                bot.quit()
                flag = 1       
        else:
            bot.quit()

def agendaarticle(wurl):
    bot = webdriver.Firefox()
    bot.get(wurl)
    page = bot.page_source
    soup = BeautifulSoup(page, 'lxml')
    bot.quit()
    title = soup.find('h1', class_ = 'node-title')
    date = soup.find('div', class_ = 'node-time text-blue')
    body = soup.find('div', class_ = 'row bodytext')
    content = body.find('div', class_ = 'col-md-12')
    paras = content.find_all('p')
    print('\n', date.text + ' -- ' + title.text.strip(), '\n')
    for para in paras:
        print(para.text, '\n')            

def newsnow():
    bot = webdriver.Firefox()
    nurl = 'https://www.newsnow.co.uk/h/World+News/Europe/Eastern+Europe/Georgia?type=ln'
    bot.get(nurl)
    newsnowcontent(bot)

def timenewsnow():
    print('Please pick your timeframe, press go and minimize the browser.')
    time.sleep(2)
    bot = webdriver.Firefox()
    nurl = 'https://www.newsnow.co.uk/h/World+News/Europe/Eastern+Europe/Georgia?type=ln'
    bot.get(nurl)
    bot.find_element_by_xpath('/html/body/div[4]/div[3]/div/div/div/div[1]/div/span').click()
    bot.find_element_by_xpath('//*[@id="nn_container"]/div[2]/main/div[2]/div/div/div[3]/div/div/span').click()
    ans = int(input('Input 0 to see the results: '))
    if ans == 0:
        newsnowcontent(bot)
    else:
        print('Please try again.')

def newsnowcontent(bot):
    page = bot.page_source
    bot.minimize_window()
    soup = BeautifulSoup(page, 'lxml')
    content = soup.find('div', class_ = 'rs-newsbox js-newsbox js-newsmain js-central_ln_wrap')
    articles = content.find_all('div', class_ = 'hl')
    print('\nFound ' + str(len(articles)) + ' results\n')
    for article in articles:
        nart = article.find('a', class_ = 'hll')
        source = article.find('span', class_ = 'src-part')
        time = article.find('span', class_ = 'time')
        print(source.text + ' - ' + time.text + ' | ' + nart.text)
        print(nart['href'], '\n')
        print('----------------------------------------------\n')  
    bot.quit()

def newsnowarticle(wurl):
    bot = webdriver.Firefox()
    bot.get(wurl)

def interpress():
    bot = webdriver.Firefox()
    iurl = 'https://www.interpressnews.ge/en/'
    bot.get(iurl)
    page = bot.page_source
    bot.minimize_window()
    soup = BeautifulSoup(page, 'lxml')
    leftcolumn = soup.find('div', class_ = 'slideritems')
    frontnews = soup.find('div', class_ = 'frontnewsin')
    lastnews = soup.find('div', class_ = 'lastnewsitems')
    lcarticles = leftcolumn.find_all('div', class_ = 'slideritem')
    fnarticles = frontnews.find_all('div', class_ = 'frontnewsitem homepagearticles')
    lnarticles = lastnews.find_all('div', class_ = 'lastnewsitem')
    print('\nFound ' + str(len(lcarticles) + len(fnarticles) + len(lnarticles)) + ' results\n')
    for lcarticle in lcarticles:
        lcdate = lcarticle.find('div', class_ = 'sliderdate_str')
        lclink = lcarticle.find('div', class_ = 'slidertitle').a
        print(lcdate.text + ' -- ' + lclink.text)
        print('https://www.interpressnews.ge' + lclink['href'], '\n')
        print('----------------------------------------------\n')
    for fnarticle in fnarticles:
        fndate = fnarticle.find('div', class_ = 'frontnewsdate')
        fnlink = fnarticle.find('div', class_ = 'frontnewstitle').a
        print(fndate.text + ' -- ' + fnlink.text)
        print('https://www.interpressnews.ge' + fnlink['href'], '\n')
        print('----------------------------------------------\n')
    for lnarticle in lnarticles:
        lndate = lnarticle.find('div', class_ = 'lastnewsdate')
        lnlink = lnarticle.find('div', class_ = 'lastnewstitle').a
        print(lndate.text + ' -- ' + lnlink.text)
        print('https://www.interpressnews.ge' + lnlink['href'], '\n')
        print('----------------------------------------------\n')    
    flag = int(input('Input 0 to see more results or input 1 to view an article: ')) 
    if flag == 0:
        bot.find_element_by_class_name('lastnewsmore').click()
        moreinterpress(bot, lnarticles, flag)   
    else:
        bot.quit()

def moreinterpress(bot, lnarticles, flag):        
    readart = len(lnarticles)
    while flag == 0:
        page = bot.page_source
        soup = BeautifulSoup(page, 'lxml')       
        morelnart = soup.find_all('div', class_ = 'lastnewsitem')
        allart = len(morelnart)
        print('\nFound ' + str(allart - readart) + ' results\n')
        while((readart) < allart):
            readart += 1
            date = morelnart[readart - 1].find('div', class_ = 'lastnewsdate')
            link = morelnart[readart - 1].find('div', class_ = 'lastnewstitle').a
            print(date.text + ' -- ' + link.text)
            print('https://www.interpressnews.ge' + link['href'], '\n')
            print('----------------------------------------------\n')
            if readart == allart:
                break
        more = int(input('Input 0 to see more results or input 1 to view an article: '))          
        if more == 0:
            try:
                for i in range(0,2):
                    bot.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(2)               
            except:
                print('Failed to retrieve more results.')
                bot.quit()
                flag = 1
        else:
            bot.quit()

def interpressarticle(wurl):
    bot = webdriver.Firefox()
    bot.get(wurl)
    page = bot.page_source
    soup = BeautifulSoup(page, 'lxml')
    bot.quit()
    content = soup.find('div', class_ = 'topcontentleft')
    category = content.find('div', class_ = 'articlecatname').a.span
    date = content.find('div', class_ = 'articledate').span
    title = content.find('h1', class_ = 'articletitle') 
    paras = content.find('div', class_ = 'articlecontent_in').find_all('p')
    print('\n',category.text + date.text + ' -- ' + title.text, '\n')
    for para in paras:
        print(para.text, '\n')

def presidentgov():
    purl = 'https://www.president.gov.ge/eng/pressamsakhuri/siakhleebi.aspx'
    presidentgovcontent(purl)

def timepresidentgov(pfromdate, ptodate):
    purl = 'https://www.president.gov.ge/eng/pressamsakhuri/siakhleebi.aspx?from=' + pfromdate + '&to=' + ptodate
    presidentgovcontent(purl)

def presidentgovcontent(purl):
    page = requests.get(purl)  
    soup = BeautifulSoup(page.content, 'lxml')
    flag, i = 0, 0
    while flag == 0:
        content = soup.find('div', class_ = 'LeftNews')
        articles = content.find_all('div', class_ = 'NewsBoxOther')
        print('\nFound ' + str(len(articles)) + ' results\n')
        for article in articles:
            date = article.find('span', class_ = 'DateBox')
            link = article.find('div', class_ = 'NewsBoxOtherTitle').h3.a
            print(date.text.strip() + ' -- ' + link.text)
            print('https://www.president.gov.ge' + link['href'], '\n')
            print('----------------------------------------------\n')
        flag = int(input('Input 0 to see more results or input 1 to view an article: '))
        if flag == 0:
            try:
                i += 1
                if i == 1:
                    bot = webdriver.Firefox()
                    bot.get(purl)
                    bot.minimize_window() 
                bot.find_element_by_class_name('NextPage').click() 
                time.sleep(1)
                page = bot.page_source
                soup = BeautifulSoup(page, 'lxml')
            except:
                print('Failed to retrieve more results.')
                bot.quit()
                flag = 1
        else:
            bot.quit()

def presidentgovarticle(wurl):
    article = requests.get(wurl)
    soup = BeautifulSoup(article.content, 'lxml')
    paras = soup.find('div', class_ = 'InsideNewsBox')
    print(paras.text)


print('Please choose the website you would like to get news from.')
time.sleep(1)
website = int(input('Input 1 for civil, 2 for agenda, 3 for newsnow, 4 for interpress, 5 for President of Georgia: '))
if website == 1:
    cnews = int(input('Input 0 to get the news feed or input 1 to get the news in a specific time frame: '))
    if cnews == 0:
        civil()
    else:    
        cfromdate = input('Please input the earliest date(in ddmmyyyy format): ')
        time.sleep(1)
        ctodate = input('Please input the latest date(in ddmmyyyy format): ')
        timecivil(cfromdate, ctodate)
elif website == 2:
    anews = int(input('Input 0 to get the news feed or input 1 to get the news in a specific time frame: '))
    if anews == 0:
        agenda()
    else:
        y = input('Please input the year(2013-2020 or all): ')
        time.sleep(1)
        m = input('Please input the month(january-december or all): ')
        timeagenda(y, m)
elif website == 3:
    nnews = int(input('Input 0 to get the news feed or input 1 to get the news in a specific time frame: '))
    if nnews == 0:
        newsnow()   
    else:
        timenewsnow()
elif website == 4:
    interpress()
elif website == 5:
    pnews = int(input('Input 0 to get the news feed or input 1 to get the news in a specific time frame: '))
    if pnews == 0:
        presidentgov()
    else:
        print('\nYou can only search articles by month, for each year.\n')
        time.sleep(1)
        pfromdate = input('Please input the first day of the month(yyyy-mm-dd e.g 2020-5-1): ')
        time.sleep(1)
        ptodate = input('Please input the last day of the month(yyyy-mm-dd e.g 2020-5-31): ')
        timepresidentgov(pfromdate, ptodate)    
flag = 0
while(flag == 0):  
    print('\nPlease copy the url in order to view one of the above articles.\n')
    time.sleep(1)
    wurl = input('Input the url or input 1 to exit the program: ')  
    if wurl == '1':
        flag = 1
    else:
        if website == 1:
            civilarticle(wurl)
        elif website == 2:
            agendaarticle(wurl) 
        elif website == 3:
            newsnowarticle(wurl)
        elif website == 4:
            interpressarticle(wurl)    
        elif website == 5:
            presidentgovarticle(wurl)    
