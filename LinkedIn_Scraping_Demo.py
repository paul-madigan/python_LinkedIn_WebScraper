from selenium import webdriver

local_chromedriver_exe = "C:\\Users\\paul.madigan\\Selenium\\ChromeDriver\\chromedriver.exe"
driver = webdriver.Chrome(local_chromedriver_exe)

driver.get("https://www.linkedin.com/in/patrickwylie/")
# driver.get("https://www.linkedin.com/in/anthony-prado-207b5599/")

input("Press Enter to continue...")

""" About """
abuotText = driver.find_element_by_xpath("//h2[text()='About']/../../p").text
print("About: ", abuotText)



""" Experience """
jobTitleText = driver.find_element_by_xpath("//h2[text()='Experience']/../..//h3").text
print("Job Title: ", jobTitleText)

companyText = driver.find_element_by_xpath("//h2[text()='Experience']/../..//h4").text
print("Company: ", companyText)

lengthofServiceText = driver.find_element_by_xpath("//h2[text()='Experience']/../..//p").text
print("Length of Service: ", lengthofServiceText)

locationText = driver.find_element_by_xpath("//h2[text()='Experience']/../..//p[@class='experience-item__location experience-item__meta-item']").text
print("Location: ", locationText)

jobDescriptionText = driver.find_element_by_xpath("//h2[text()='Experience']/../..//p[@class='show-more-less-text__text--less']").text
print("Job Description: ", jobDescriptionText)



""" Education """
schoolText = driver.find_element_by_xpath("//h2[text()='Education']/../..//h3[@class='result-card__title']").text
print("School: ", schoolText)

degreeText = driver.find_element_by_xpath("//h2[text()='Education']/../..//h4").text
print("Degree: ", degreeText)

yearsText = driver.find_element_by_xpath("//h2[text()='Education']/../..//p").text
print("Years: ", yearsText)



""" Licenses & Certifications """
certificationNameText = driver.find_element_by_xpath("//h2[text()='Licenses & Certifications']/../..//h3").text
print("Certification Name: ", certificationNameText)

issuingBodyText = driver.find_element_by_xpath("//h2[text()='Licenses & Certifications']/../..//h4").text
print("Issuing Body: ", issuingBodyText)

issueDateText = driver.find_element_by_xpath("//h2[text()='Licenses & Certifications']/../..//span").text
print("Issue Date: ", issueDateText)

credentialIDText = driver.find_element_by_xpath("//h2[text()='Licenses & Certifications']/../..//div[@class='certifications__credential-id']").text
print("Credentials ID: ", credentialIDText)


