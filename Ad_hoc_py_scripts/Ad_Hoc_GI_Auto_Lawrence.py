import asyncio
from pyppeteer import launch
import nest_asyncio
import time
import re

# Apply the nest_asyncio patch
nest_asyncio.apply()

async def access_website():
    browser = await launch(headless=False,executablePath='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',)  # Set headless to False to see browser in action
    page = await browser.newPage()  # Create a new tab
    await page.setViewport({
    'width': 1100,
    'height': 800,
    'deviceScaleFactor': 1,
    'isMobile': False,
    'hasTouch': False,
    'isLandscape': False
})
    
    
    chosen_client = 'UK Molson Coors'
    chosen_product = 'UK Molson Coors'
    username = 'rob.manley@onclusive.com'
    password = 'Password*1'
    
    # Navigate to the desired webpage
    await page.goto('https://aweprodrepcasmaceweb.azurewebsites.net/InsightScoring/Index#')
    
    
    #LOGIN PAGE
    
    
    #waits for the username box to appear
    #await page.waitForSelector('#User')
    
    time.sleep(1)
    # Fill in the username and password fields
    await page.type('#user', username)  # Replace 'your_username' with your actual username
    await page.type('#password', password)  # Replace 'your_password' with your actual password
    time.sleep(1)
    await page.click('#btnLogin') #click on the login button
    
    
    # SEARCH/FILTER PAGE
    
    # Once logged on, waiting for the client dropdown element and search button to show
    await page.waitForSelector('span.k-icon.k-i-arrow-60-down', timeout=10000)
    await page.waitForSelector('#btnSearch')
    
    #Scanning the webpage for all the textboxes and storing their xpath locations in a list
    
    text_boxes = await page.xpath('//*[@class="k-textbox"]')
    
    # Identifying the client dropdown menu and scrolling it into view
    selector = 'span.k-icon.k-i-arrow-60-down'
    await page.evaluate('''selector => {
        const element = document.querySelector(selector);
        if (element) {
            element.scrollIntoView();
        }
    }''', selector)
    
    # clicking on the client dropdown menu
    await page.click('span.k-icon.k-i-arrow-60-down')
    
    # waiting x seconds so that the webpage can catch up with Python
    time.sleep(1)
    
    # Typing an empty string into the textbox so that options show
    await text_boxes[0].type(' ')
    
    # waiting x seconds
    await page.waitFor(2000) 
    
    #Holding down the donw key so that we can see all the clients available in the dropdown
    for x in range(0,1000):
                   await page.keyboard.press('ArrowDown')
                   clients = await page.evaluate('''() => {
        const items = Array.from(document.querySelectorAll('#ClientDetailsPicker_listbox .k-item'));
        return items.map(item => ({
            text: item.innerText,
            value: item.getAttribute('data-uid')
        }));
    }''')
                
    # Release the ArrowDown key
    await page.keyboard.up('ArrowDown')

    # Typing the client into the textbox
    await page.keyboard.press('Backspace')
    await text_boxes[0].type(chosen_client)
    
    # waiting x seconds for the webpage to catch up with Python
    time.sleep(1)
    
    # setting the chosen client xpath
    client_xpath = f"//li[contains(text(), '{chosen_client}')]"
    
    # waiting for the client to appear in list
    await page.waitForXPath(client_xpath, timeout=10000)
    
    # find the chosen client in the dropdown list
    client_elements = await page.xpath(client_xpath)
    
    # clicking on client
    await client_elements[0].click()
    
    await page.waitFor(2000)  # wait for 2 seconds
    
    # selecting the date button
    button = await page.querySelector('#scoringDateRange')
    
    #clicking the date button
    await button.click()
    
    # looking for 'this year' from the list that appears - can chane to any time period
    li_elements = await page.xpath('//li[text()="This Year"]')
    
    # waiting x secs and clicking the button
    time.sleep(1)
    await li_elements[0].click()

    # searching for the product filter button
    product_handle = await page.xpath('//*[@id="productGroupFilterContainer"]/div/span/span/span[2]/span')
    
    # clicking product filter button
    await product_handle[0].click()

    await page.waitFor(2000)  # wait for 2 seconds
    
    # pressing arrowing down and printing the products
    for x in range(0,30):
                   await page.keyboard.press('ArrowDown')
                   products = await page.evaluate('''() => {
        const items = Array.from(document.querySelectorAll('#ProductGroupPicker_listbox .k-item'));
        return items.map(item => ({
            text: item.innerText,
            value: item.getAttribute('data-uid')
        }));
    }''')

    # typing the chosen product into the textbox
    element_handle = text_boxes[1]
    await element_handle.type(chosen_product)

    print('1 complete')

    #waiting for the chosen product to appear in the dropdown menu
    await page.waitForSelector("#ProductGroupPicker_listbox > li.k-virtual-item.k-item.k-state-selected.k-state-focused", {'visible': True})

    print('2 complete')

    # Find the specific item under 'ProductGroupPicker_listbox'
    items = await page.JJ("#ProductGroupPicker_listbox > li.k-virtual-item.k-item.k-state-selected.k-state-focused")

    print (items)

    print('3 complete')

    time.sleep(1)
    
    # 
    delivered_handle = await page.xpath(' //*[@id="filter"]/div[3]/input[1]')
    await delivered_handle[0].click()

    time.sleep(1)

    print('4 complete')

    delivered_handle = await page.xpath(' //*[@id="filter"]/div[3]/input[1]')
    await delivered_handle[0].click()

    time.sleep(.5)

    print('5 complete')
    
    # Identifying and pressing the login button
    login_handle = await page.xpath('//*[@id="btnSearch"]')
    await login_handle[0].click()
    
    loading_text_selector = '.loading-text'
    await page.waitForSelector(loading_text_selector, {'hidden': True })

    print('All complete')
    
#Execute the function
asyncio.get_event_loop().run_until_complete(access_website())