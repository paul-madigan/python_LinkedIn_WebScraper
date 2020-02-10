from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import random
import re

url_regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'


""" Initialize CSV """
# Classification - Experience -> 1
# Anything Else -> 0
with open('LI_Block_Data.csv', 'a', newline='') as block_file, open('LI_Sentence_Data.csv', 'a', newline='') as sentence_file:
# with open('LI_Block_Data.csv', 'w', newline='') as block_file, open('LI_Sentence_Data.csv', 'w', newline='') as sentence_file:
    block_writer = csv.writer(block_file)
    sentence_writer = csv.writer(sentence_file)


    """ Use Chrome profile in new Chrome window """
    options = Options()
    options.add_argument('--user-data-dir=C:/Users/paul.madigan/AppData/Local/Google/Chrome/User Data/Profile 1')
    options.add_argument("start-maximized")
    local_chromedriver_exe = "C:\\Users\\paul.madigan\\Selenium\\ChromeDriver\\chromedriver.exe"

    driver = webdriver.Chrome(executable_path=local_chromedriver_exe, chrome_options=options)
    original_window = driver.current_window_handle  # Store the ID of the original window
    # company = "accenture"
    company = "facebook"
    url = "https://www.linkedin.com/company/" + company + "/people/?keywords="

    letterlistA = ["a", "e", "i", "o", "u"]
    letterlistB = ["j", "h", "g", "f", "d", "a", "e", "i", "o", "u", "l", "r", "t", "p", "k"]
    for letter in letterlistB:
        searchkey = letter + random.choice(letterlistA)
        driver.get(url + searchkey)

    # namelist = ["James", "Mark", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elicia", "David", "Richard", "Susanna", "Joe", "Jessie", "Thomas", "Sarah", "Charles", "Karen", "Chris", ""]
    # for name in namelist:
    #     driver.get(url + name)

        time.sleep(5)
        """ Search for users """
        # peopleSearchBox = driver.find_element_by_xpath("//input[@id='people-search-keywords']")
        # peopleSearchBox.send_keys('b')
        # peopleSearchBox.send_keys(Keys.ENTER)

        x = 0
        while x < 10:
            driver.find_element_by_xpath("//html[1]").send_keys(Keys.END)
            time.sleep(10)
            x = x+1

        time.sleep(3)
        totalTileNumber = len(driver.find_elements_by_xpath("//ul[@class='org-people-profiles-module__profile-list']/li"))
        print(totalTileNumber)
        for tileNumber in range(1, (totalTileNumber + 1)):
            try:
                # Get the person's tile and open it in a new chrome tab
                personTile = driver.find_element_by_xpath(
                    "//li[@class='org-people-profiles-module__profile-item'][{}]//a[@data-control-name='people_profile_card_name_link']".format(
                        tileNumber))
                builder = ActionChains(driver)
                builder.move_to_element(personTile).perform()
                link_to_click = personTile.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(3)

                # Once the new tab opens, save the current tab ID and switch windows to the new tab
                driver.switch_to.window(driver.window_handles[1])

                """ Get Experience """
                totalExperienceInstances = len(driver.find_elements_by_xpath("//h2[text()='Experience']/../../ul/li"))
                for experienceInstance in range(1, (totalExperienceInstances + 1)):
                    if driver.find_element_by_xpath(
                            "//h2[text()='Experience']/../..//li[{}]".format(experienceInstance)).is_displayed():
                        try:
                            experienceText = driver.find_element_by_xpath(
                                "//h2[text()='Experience']/../..//li[{}]//div[@class='pv-entity__extra-details ember-view']".format(
                                    experienceInstance)).text
                            expEditText = experienceText.replace("=", "").replace("-", "").replace(",", "").replace("…", "").replace(
                                "see more", "").replace("\n", " ").strip().replace("•", ".").replace("·", ".").replace("*", "").replace(">", "")
                            expEditText = re.sub(r'[ ]{2,}', " ", expEditText)  # replaces any instance of more than one space being used
                            urlList = re.findall(url_regex, expEditText)
                            for url in urlList:
                                sentence_writer.writerow([url, "0"])
                            expEditText = re.sub(url_regex, "", expEditText)  # removes urls
                            block_writer.writerow([expEditText, "1"])
                            print(expEditText)
                            # split the text up by period
                            splitTextList = expEditText.split('.')
                            for line in splitTextList:
                                full_line = line + "."  # Adding in period
                                sentence_writer.writerow([full_line, "1"])
                        except Exception as e:
                            print("Unable to find experience text. \n", e)

                """ Get Education """
                totalEducationInstances = len(driver.find_elements_by_xpath("//h2[text()='Education']/../../ul/li"))
                for educationInstance in range(1, (totalEducationInstances + 1)):
                    if driver.find_element_by_xpath(
                            "//h2[text()='Education']/../..//li[{}]".format(educationInstance)).is_displayed():
                        try:
                            educationText = driver.find_element_by_xpath(
                                "//h2[text()='Education']/../..//li[{}]".format(educationInstance)).text
                            # uniName = driver.find_element_by_xpath("//h2[text()='Education']/../..//li[{}]//h3".format(educationInstance)).text
                            # degreeName = driver.find_element_by_xpath("//h2[text()='Education']/../..//li[{}]//span[@class='pv-entity__comma-item']".format(educationInstance)).text
                            eduEditText = educationText.replace("=", "").replace("-", " ").replace(",", "").replace("…", "").replace(
                                "see more", "").replace("\n", " ").strip().replace("Degree Name", " ").replace(
                                "Field Of Study", " ").replace("Dates attended or expected graduation", " ").replace(
                                "Dates attended or expected graduation", " ").replace("Activities and Societies:", " ").replace("•", ".").replace("·", ".").replace("*", "").replace(">", "")
                            eduEditText = re.sub(r'[ ]{2,}', " ", eduEditText)  # replaces any instance of more than one space being used
                            urlList = re.findall(url_regex, eduEditText)
                            for url in urlList:
                                sentence_writer.writerow([url, "0"])
                            eduEditText = re.sub(url_regex, "", eduEditText)  # removes urls
                            block_writer.writerow([eduEditText, "0"])
                            # splitTextList = expEditText.split('.')
                            splitTextList = re.split(r'[a-zA-Z]{2,}\.', LicCertEditText)  # Will only split strings by the delimiter of a period preceded by 2 or more alphanumeric character
                            for line in splitTextList:
                                full_line = line + "."  # Adding in period
                                sentence_writer.writerow([full_line, "0"])
                        except Exception as e:
                            print("Unable to find education text. \n", e)

                """ Get Licenses and Certifications """
                totalLicCertInstances = len(
                    driver.find_elements_by_xpath("//h2[text()='Licenses & Certifications']/../../ul/li"))
                for LicCertInstance in range(1, (totalLicCertInstances + 1)):
                    if driver.find_element_by_xpath("//h2[text()='Licenses & Certifications']/../..//li[{}]".format(
                            LicCertInstance)).is_displayed():
                        try:
                            LicCertText = driver.find_element_by_xpath(
                                "//h2[text()='Licenses & Certifications']/../..//li[{}]".format(LicCertInstance)).text
                            LicCertEditText = LicCertText.replace("=", "").replace("-", " ").replace(",", " ").replace("…", "").replace(
                                "see more", "").replace("\n", " ").strip().replace("Issuing authority", " ").replace(
                                " Issued date and  if applicable  expiration date of the certification or license",
                                " ").replace("•", ".").replace("·", ".").replace("No Expiration Date", "").replace("*", "").replace(">", "")
                            LicCertEditText = re.sub(r'[ ]{2,}', " ", LicCertEditText)  # replaces any instance of more than one space being used
                            urlList = re.findall(url_regex, LicCertEditText)
                            for url in urlList:
                                sentence_writer.writerow([url, "0"])
                            LicCertEditText = re.sub(url_regex, " ", LicCertEditText)  # removes URLs
                            block_writer.writerow([LicCertEditText, "0"])
                            # splitTextList = LicCertEditText.split('.')
                            splitTextList = re.split(r'[a-zA-Z]{2,}\.', LicCertEditText)  # Will only split strings by the delimiter of a period preceded by 2 or more alphanumeric character
                            for line in splitTextList:
                                full_line = line + "."  # Adding in period
                                sentence_writer.writerow([full_line, "0"])
                        except Exception as e:
                            print("Unable to find licenses and Certifications text. \n", e)

                # Close current tab and switch to original
                driver.close()
                driver.switch_to.window(original_window)  # Switch back to original tab
                time.sleep(2)
            except Exception as e:
                print("Unable to find tile, Moving to next. \n", e)


