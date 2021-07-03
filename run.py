## Credentials & URL
excardUsername = input("Please enter Excard username:\n")
excardPassword = input("Please enter Excard password:\n")

loginUrl       = "https://www.excard.com.my/home-visitor"
priceListUrl   = "https://www.excard.com.my/price-list-new/Digital/52"

## Options Available
catOptions    = ['Custom Die-Cut', 'Rectangle/Square', 'Round', 'Standard Shape', 'Multiple Dieline']
cutOptions    = ['Cut To Size', 'Die-Cutting']
paperOptions  = ['Mirror Kote', 'Printing Paper', 'Transparent OPP', 'Removable Transparent OPP',
    'Synthetic Paper', 'White PP (Polypropylene)', 'Bright Silver Polyester',
    'Matte Silver Polyester', 'Removable White PP', 'Brown Craft Paper', 'Warranty Sticker']
finishOptions = ['Not Required', 'Matte Laminate (Front)', 'Gloss Laminate (Front)',
    'Gloss Water Based Varnish', 'UV Varnish', 'Soft Touch Laminate (Front)']

## Options to execute
catExecutables    = ['Round']
cutExecutables    = ['Die-Cutting']
paperExecutables  = ['Synthetic Paper']
finishExecutables = ['Not Required', 'Matte Laminate (Front)', 'Gloss Laminate (Front)', 'UV Varnish']

## Dimensions
minHeight = 10
maxHeight = 300

minWidth = 25
maxWidth = 420

dimStep = 1

################################################################################
## END OF USER CONFIGURATION
################################################################################

import os
import time
import itertools

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select

import pandas as pd
from bs4 import BeautifulSoup

################################################################################

## Initialize browser
driver = webdriver.Edge("lib\edgedriver_win32\msedgedriver.exe")
print('Initialize browser')

## Define useful functions
def wait():
    driver.implicitly_wait(10)
    try:
        element_present = EC.invisibility_of_element_located((By.ID, "UpdateProgress1"))
        WebDriverWait(driver, 30).until(element_present)

    except TimeoutException:
        print("Timed out waiting for page to load")

def navigate(url):
    driver.get(url)
    print('Navigate to '+url)

def fill(target, value):
    driver.find_element_by_id(target).send_keys(value)

def clear(target):
    driver.find_element_by_id(target).clear()

def click(target):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, target)))
    driver.find_element_by_id(target).click()
    wait()

def select(target, value):
    Select(driver.find_element_by_id(target)).select_by_visible_text(value)
    wait()

def check(target):
    checkbox = driver.find_element_by_id(target)
    while not checkbox.is_selected():
    	checkbox.click()

def scrollTo(target):
    element = driver.find_element_by_id(target)
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    time.sleep(3)

def scrollTop():
    element = driver.find_element_by_id("mainContent_price_list_sticker1_rblOrderType_0")
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    time.sleep(3)

def removeDuplicates(ls):
    return sorted(sorted(list({*map(tuple, map(sorted, ls))}), key=lambda x: x[0]), key=lambda x: x[1])

def exportExcel(name):
    trials = 0
    print('Preparing data to export...')

    try:
        soup = BeautifulSoup(driver.page_source, "lxml")
        div = soup.select_one("#mainContent_price_list_sticker1_tblPriceList")
        table = pd.read_html(str(div))

        df = table[0].iloc[4:]
        df.to_excel(name+".xlsx", index=False, header=False)

    except Exception as e:
        print('Failed to scrape data. Retrying...')
        trials = trials+1

        if trials < 5:
            time.sleep(3)
            exportExcel(name)
        else:
            trials = 0

            click("mainContent_price_list_sticker1_btnGenerate")
            wait()

            time.sleep(10)
            exportExcel(name)


################################################################################

## Login to Excard
navigate(loginUrl)

fill("TemplatedContent1__login_txtusername", excardUsername)
fill("TemplatedContent1__login_txtPassword", excardPassword)

print('Fill up login credentials')

try:
    click("TemplatedContent1__login_excardLogin")
except Exception as e:
    click("excard-form-btnclose")
    click("TemplatedContent1__login_excardLogin")

print('Logged in')

## Navigate to sticker price list
navigate(priceListUrl)
print('Start scraping task...')

################################################################################

## Generate all option combinations
options = [catExecutables, cutExecutables, paperExecutables, finishExecutables]
options = list(itertools.product(*options))

currentCategory = ''

for option in options:

    scrollTop()

    ## Set category
    category = option[0]
    catIndex = catOptions.index(category)

    ## If category is excluded
    # if category in catExcludes:
    #     print('Category "'+category+'" is excluded. Skipping..')
    #     continue

    click("mainContent_price_list_sticker1_rdcategory_"+str(catIndex))
    print('Set category as "'+category+'"')

    ############################################################################

    ## Select quantities
    if category != currentCategory:
        scrollTo('mainContent_price_list_sticker1_ddlfinishing')
        # time.sleep(3)

        check('mainContent_price_list_sticker1_cblQty_1') # 1,500 - 10,000
        check('mainContent_price_list_sticker1_cblQty_2') # 15,000 - 100,000
        check('mainContent_price_list_sticker1_cblQty_3') # 150,000 - 1,000,000

        print('Select all quantities')

    currentCategory = category

    ############################################################################

    scrollTop()

    ## Set cutting method
    cutting = option[1]
    cutIndex = cutOptions.index(cutting)

    ## If cutting is excluded
    # if cutting in cutExcludes:
    #     print('Cutting method "'+cutting+'" is excluded. Skipping..')
    #     continue

    ## When category = "Rectangle/Square"
    if category == "Rectangle/Square":
        click("mainContent_price_list_sticker1_rblCuttingMethod_"+str(cutIndex))
        print('Set cutting method as "'+cutting+'"')

        ## When cutting = "Cut To Size"
        if cutting == "Cut To Size":
            minHeight = 54
            minWidth = 89

    ## When category = "Round"
    if category == "Round":
        minHeight = 15 # 1~10 only applicable for "Warranty Sticker"

    ## Check for cutting method supports
    if category != "Rectangle/Square" and cutting == "Cut To Size":
        print('Cutting method "'+cutting+'" is not supported. Skipping..')
        continue

    ############################################################################

    ## Set paper
    paper = option[2]
    paperIndex = paperOptions.index(paper)

    ## Set finishing
    finish = option[3]
    finishIndex = finishOptions.index(finish)

    ############################################################################

    ## Skip finishing
    if category == "Round" and cutting == "Die-Cutting" and paper == "Synthetic Paper" and finish == "Not Required":
        print('Skip finishing "', finish, '"')
        continue

    ## Skip dimension
    if category == "Round" and cutting == "Die-Cutting" and paper == "Synthetic Paper" and finish == "Matte Laminate (Front)":
        minHeight = 123

    ############################################################################

    ## Generate all dimension combinations
    H = list(range(minHeight, maxHeight+1, dimStep))
    W = list(range(minWidth, maxWidth+1, dimStep))

    if category == "Round":
        dimensions = H
    else:
        dimensions = removeDuplicates(list(itertools.product(*[H, W])))

    for dim in dimensions:
        start = time.time()

        scrollTop()
        # time.sleep(3)

        ## Set diameter if category == "Round"
        if category == "Round":
            dimension = str(dim)
            print('Set diameter as', dim)
            fill("mainContent_price_list_sticker1_txtDiameter", dim)

            click("mainContent_price_list_sticker1_txtDiameter")
            time.sleep(3)

        ## Else, set dimensions
        else:
            dimension = str(dim[0])+'x'+str(dim[1])
            print('Set dimension as '+dimension)

            fill("mainContent_price_list_sticker1_txtHeight", dim[0])
            click("mainContent_price_list_sticker1_txtWidth")

            time.sleep(3)

            fill("mainContent_price_list_sticker1_txtWidth", dim[1])
            click("mainContent_price_list_sticker1_txtHeight")

            time.sleep(3)

        ########################################################################

        ## If paper is excluded
        # if paper in paperExcludes:
        #     print('Paper "'+paper+'" is excluded. Skipping..')
        #     continue

        ## Check for "Warranty Sticker" supports
        if category in ["Custom Die-Cut", "Multiple Dieline"] and paper == "Warranty Sticker":
            print('Paper "'+paper+'" is not supported. Skipping..')
            continue

        select("mainContent_price_list_sticker1_ddlPaper", paper)
        print('Set paper as "'+paper+'"')

        ########################################################################

        ## If finishing is excluded
        # if finish in finishExcludes:
        #     print('Finishing "'+finish+'" is excluded. Skipping..')
        #     continue

        ## Check for finishing supports
        catWithoutFinish = ["Printing Paper", "Bright Silver Polyester", "Matte Silver Polyester", "Brown Craft Paper"]

        if paper in catWithoutFinish and finishIndex > 0:
            print('Finishing "'+finish+'" is not supported. Skipping..')
            continue

        if finish == "Gloss Water Based Varnish" and paper != "Mirror Kote":
            print('Finishing "'+finish+'" is not supported. Skipping..')
            continue

        if finish in ["Gloss Water Based Varnish", "UV Varnish"] and paper == "Removable White PP":
            print('Finishing "'+finish+'" is not supported. Skipping..')
            continue

        if not paper in catWithoutFinish:
            select("mainContent_price_list_sticker1_ddlfinishing", finish)
            print('Set finishing as "'+finish+'"')

        ########################################################################

        ## Generate price list
        scrollTo('mainContent_price_list_sticker1_ddlfinishing')
        # time.sleep(3)

        click("mainContent_price_list_sticker1_btnGenerate")
        print('Generating price list')
        wait()

        time.sleep(5)

        ## Export
        dirName = "/".join(['export', 'CAT='+category, 'CUT='+cutting, 'PP='+paper, 'FIN='+finish])
        filename = 'pricelist_'+dimension+'mm'

        if not os.path.exists(dirName):
            os.makedirs(dirName)

        exportExcel(dirName+'/'+filename)

        end = time.time()
        elapsed = end - start

        print('Price list is exported successfully in '+str(elapsed)+'s')
        print('Preparing for next task...')

        ## Clear dimension input
        if category == "Round":
            clear("mainContent_price_list_sticker1_txtDiameter")
            time.sleep(3)

        ## Else, set dimensions
        else:
            clear("mainContent_price_list_sticker1_txtHeight")
            time.sleep(3)

            clear("mainContent_price_list_sticker1_txtWidth")
            time.sleep(3)

print('End of script execution')
