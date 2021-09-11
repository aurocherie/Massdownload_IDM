#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Std Library
import time
import sys, getopt

# check if selenium download finish or timeout
#def download_wait(time_out):
    #seconds = 0
    #dl_wait = True
    #while dl_wait and seconds < time_out:
#        time.sleep(1)
        #dl_wait = False
        #for fname in os.listdir("."):
    #        if fname.endswith('.crdownload'):
#                dl_wait = True
        #seconds += 1
    #return seconds

# Get shopping list
def main(argv):

 input_file = ''

 try:
# Process args
     opts, args = getopt.getopt(argv,"i:c:",["ifile="])
 except getopt.GetoptError:
      print ('massdownload_F4E.py -i listfile -c credentials.txt')
      sys.exit(2)
 for opt, arg in opts:
      if opt == '-h':
         print ('massdownload_F4E.py -i listfile')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         input_file = arg
      elif opt in ("-c", "--cfile"):
         cred_file = arg
 print ('Input file is ', input_file)
 print ('Credentials file is ', cred_file)

# Open shopping list
 shop_file = open(input_file,"r")
 shopping_list = shop_file.read().splitlines()
 print('Shopping list contains ', len(shopping_list), ' files')
 print('Shopping List : ', shopping_list )
 shop_file.close()

# Open credentials file
 creds_file = open(cred_file,"r")
 credentials_list = creds_file.read().splitlines()
 print('Credentials contains ', len(credentials_list), ' lines')
 print('Credentials : ', credentials_list )
 creds_file.close()

# Init selenium
 options = webdriver.ChromeOptions()
#options.add_argument("-headless")
#options.add_argument("-disable-gpu")
 prefs = {}
 prefs["profile.default_content_settings.popups"]=0
 prefs["download.default_directory"]="/tmp/F4E_Idm_download"
 options.add_experimental_option("prefs", prefs)

 PATH = "/local/home/ronan/soft/IO_Idm/chromedriver_linux64/chromedriver"
 driver = webdriver.Chrome(options=options, executable_path=PATH)

# Launch login page
 try:
      # Connexion to one target page to get rid of login
      driver.set_window_size(1200, 1000)
      driver.get('https://idm.f4e.europa.eu/default.aspx?uid=2FB7AW')
      print(driver.title)
      print("..found")
 except:
       driver.quit()

 # Manage login
 login_field = driver.find_element_by_id("username")
 login_field.send_keys(credentials_list[0])
 pwd_field = driver.find_element_by_id("password")
 pwd_field.send_keys(credentials_list[1])
 pwd_field.send_keys(Keys.RETURN)

 # Main loop
 for x in shopping_list:
          print("Traitement UID :",x)

          # Connexion to target page
          path_looked = "https://idm.f4e.europa.eu/default.aspx?uid="+x+"&action=get_document"
          print(path_looked)
          driver.get(path_looked)
          #print(driver.title)
          print("..found")

          # enter credentials
          pwd_field = driver.find_element_by_id("password")
          pwd_field.send_keys(credentials_list[1])
          pwd_field.send_keys(Keys.RETURN)

          # check if download complete
#          if (download_wait(10) == 10):
              #print("pending download")
          time.sleep(10)
          print("fin 10sec")

 driver.quit()

if __name__ == "__main__":
   main(sys.argv[1:])
