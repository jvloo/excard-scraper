## Credentials & URL
excardUsername = ""
excardPassword = ""

loginUrl = "https://www.excard.com.my/home-visitor"
priceListUrl = "https://www.excard.com.my/price-list-new/Digital/52"

## Category options
catOptions = ['Custom Die-Cut', 'Rectangle/Square', 'Round', 'Standard Shape', 'Multiple Dieline']
catExcludes = ['Multiple Dieline']

## Cutting options
cutOptions = ['Cut To Size', 'Die-Cutting']
cutExcludes = []

## Paper options
paperOptions = ['Mirror Kote', 'Printing Paper', 'Transparent OPP', 'Removable Transparent OPP',
    'Synthetic Paper', 'White PP (Polypropylene)', 'Bright Silver Polyester',
    'Matte Silver Polyester', 'Removable White PP', 'Brown Craft Paper', 'Warranty Sticker']

paperExcludes = []

## Finishing options
finishOptions = ['Not Required', 'Matte Laminate (Front)', 'Gloss Laminate (Front)',
    'Gloss Water Based Varnish', 'UV Varnish', 'Soft Touch Laminate (Front)']

finishExcludes = []

## Dimensions
minHeight = 10
maxHeight = 300

minWidth = 25
maxWidth = 420

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

def scrollTo(target):
    element = driver.find_element_by_id(target)
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    time.sleep(3)

def scrollTop():
    element = driver.find_element_by_id("tab_container")
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    time.sleep(3)

def exportExcel(name):
    try:
        soup = BeautifulSoup(driver.page_source)
        div = soup.select_one("#mainContent_price_list_sticker1_tblPriceList")
        table = pd.read_html(str(div))

        df = table[0].iloc[4:]
        df.to_excel(name+".xlsx", index=False, header=False)

    except Exception as e:
        time.sleep(3)
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

start = time.process_time()

## Select quantities
click('mainContent_price_list_sticker1_cblQty_1') # 1,500 - 10,000
click('mainContent_price_list_sticker1_cblQty_2') # 15,000 - 100,000
click('mainContent_price_list_sticker1_cblQty_3') # 150,000 - 1,000,000

print('Select all quantities')

time.sleep(3)

################################################################################

scrollTop()

## Set category
category = catOptions[0] # options[0]
catIndex = catOptions.index(category)

## If category is excluded
if category in catExcludes:
    print('Category "'+category+'" is excluded. Skipping..')
    # continue

click("mainContent_price_list_sticker1_rdcategory_"+str(catIndex))
print('Set category as "'+category+'"')

################################################################################

## Set cutting method
cutting = cutOptions[0] # options[1]
cutIndex = cutOptions.index(cutting)

## If cutting is excluded
if cutting in cutExcludes:
    print('Cutting method "'+cutting+'" is excluded. Skipping..')
    # continue

## When category = "Rectangle/Square"
if category == "Rectangle/Square":
    click("mainContent_price_list_sticker1_rblCuttingMethod_"+str(cutIndex))
    print('Set cutting method as "'+cutting+'"')

    ## When cutting = "Cut To Size"
    if cutting == "Cut To Size":
        minHeight = 54
        minWidth = 89

## Check for cutting method supports
if category != "Rectangle/Square" and cutting == "Die-Cutting":
    print('Cutting method "'+cutting+'" is not supported. Skipping..')
    # continue

################################################################################

## Set diameter if category == "Round"
if category == "Round":
    fill("mainContent_price_list_sticker1_txtDiameter", minHeight)
    print('Set diameter as', minHeight)

    click("mainContent_price_list_sticker1_upPriceListLabelSticker")
    time.sleep(3)

    dimension = minHeight

## Else, set dimensions
else:
    fill("mainContent_price_list_sticker1_txtHeight", minHeight)
    click("mainContent_price_list_sticker1_upPriceListLabelSticker")
    time.sleep(3)

    fill("mainContent_price_list_sticker1_txtWidth", minWidth)
    click("mainContent_price_list_sticker1_upPriceListLabelSticker")
    time.sleep(3)

    dimension = str(minHeight)+'x'+str(minWidth)
    print('Set height x width as '+dimension)

################################################################################

## Set paper
paper = paperOptions[0] # options[2]
paperIndex = paperOptions.index(paper)

## If paper is excluded
if paper in paperExcludes:
    print('Paper "'+paper+'" is excluded. Skipping..')
    # continue

## Check for "Warranty Sticker" supports
if category in ["Custom Die-Cut", "Multiple Dieline"] and paper == "Warranty Sticker":
    print('Paper "'+paper+'" is not supported. Skipping..')
    # continue

select("mainContent_price_list_sticker1_ddlPaper", paper)
print('Set paper as "'+paper+'"')

################################################################################

## Set finishing
finish = finishOptions[0] # options[3]
finishIndex = finishOptions.index(finish)

## If finishing is excluded
if finish in finishExcludes:
    print('Finishing "'+finish+'" is excluded. Skipping..')
    # continue

## Check for finishing supports
catWithoutFinish = ["Printing Paper", "Bright Silver Polyester", "Matte Silver Polyester", "Brown Craft Paper"]

if paper in catWithoutFinish and finishIndex > 0:
    print('Finishing "'+finish+'" is not supported. Skipping..')
    # continue

if finish == "Gloss Water Based Varnish" and paper != "Mirror Kote":
    print('Finishing "'+finish+'" is not supported. Skipping..')
    # continue

if finish in ["Gloss Water Based Varnish", "UV Varnish"] and paper == "Removable White PP":
    print('Finishing "'+finish+'" is not supported. Skipping..')
    # continue

if not paper in catWithoutFinish:
    select("mainContent_price_list_sticker1_ddlfinishing", finish)
    print('Set finishing as "'+finish+'"')

################################################################################

## Generate price list
click("mainContent_price_list_sticker1_btnGenerate")
print('Generating price list')
wait()

time.sleep(10)

## Export
dirName = "/".join(['export', category, cutting, paper, finish])
filename = 'pricelist_'+dimension+'mm'


if not os.path.exists(dirName):
    os.makedirs(dirName)

exportExcel(dirName+'/'+filename)

print('Price list is exported to directory "'+dirName+'" successfully')
print('Time taken', time.process_time() - start)
