# WebAdvisor roster scraper
# Limitations: User can have no more than 20 sections and 100 students per section
# Author: Jeffrey Bergamini
import sys
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebAdvisor:
  def __init__(self, username, passphrase, term):
    """Logs in to WebAdvisor using the given username and passphrase. Term will be used for class ids."""
    # Log in
    self.browser = webdriver.Chrome()
    self.username = username
    self.passphrase = passphrase
    self.term = term
    self.NONLETTERS_PATTERN = re.compile(r'[^A-Za-z]+')
  def get_rosters(self):
    """
    Returns a dictionary of roster info, where keys are class ids and values are lists of dictionaries containing the following keys:
       - username
       - name
       - id
       - email
       - phone
    """
    # Log in
    self.browser.get('https://wave.cabrillo.edu')
    self.browser.find_element_by_link_text('Log In').click()
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "USER_NAME")))
    user_name_field = self.browser.find_element_by_id('USER_NAME')
    while user_name_field.get_attribute('value') != self.username:
      user_name_field.clear()
      self.browser.execute_script('document.getElementById("USER_NAME").value = "%s"' % self.username)
    passphrase_field = self.browser.find_element_by_id('CURR_PWD')
    while passphrase_field.get_attribute('value') != self.passphrase:
      passphrase_field.clear()
      self.browser.execute_script('document.getElementById("CURR_PWD").value = "%s"' % self.passphrase)
    self.browser.find_element_by_id('USER_NAME').submit()
    # Faculty menu
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Faculty")))
    self.browser.find_element_by_link_text('Faculty').click()
    ret = dict()
    # For each section...
    full_term_name = {'s': 'Spring', 'f': 'Fall'}[self.term[0]] + ' 20' + self.term[1:]
    for class_num in range(1, 20):
      WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Class Roster")))
      self.browser.find_element_by_link_text('Class Roster').click()
      WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "VAR1")))
      self.browser.execute_script('''
        document.getElementById('VAR1').selectedIndex = 1;
        var dd = document.getElementById('VAR1');
        for (var i = 0; i < dd.options.length; i++) {
            if (dd.options[i].text === '%s') {
                dd.selectedIndex = i;
                break;
            }
        }
        ''' % full_term_name)
      self.browser.find_element_by_id('VAR1').submit()
      # Select the next section
      try:
        self.browser.find_element_by_id('LIST_VAR1_%d' % class_num).click()
      except:
        break
      self.browser.find_element_by_id('LIST_VAR1_%d' % class_num).submit()
      class_name = self.browser.find_element_by_id('LIST_VAR2_1')
      class_tokens = [x.strip().lower() for x in class_name.text.split('-')]
      # Take care of CS/MATH 23 crosslisting
      if class_tokens[0] == 'math':
        class_tokens[0] = 'cs'
      # My pattern for class_id is DeptNumTerm
      class_id = class_tokens[0] + class_tokens[1] + self.term
      section_id = class_tokens[2].split()[0]
      if class_id not in ret:
        ret[class_id] = []
      # All students
      for stu_num in range(1, 100):
        try:
          stu_name = self.browser.find_element_by_id('LIST_VAR7_%d' % stu_num).text
          stu_id = self.browser.find_element_by_id('LIST_VAR6_%d' % stu_num).text
          stu_email = self.browser.find_element_by_id('LIST_VAR8_%d' % stu_num).text
          stu_phone = self.browser.find_element_by_id('VAR_LIST2_%d' % stu_num).text
          name_tokens = [x.strip().lower() for x in stu_name.split(',')]
          # My pattern for usernames is e.g. FirstInitialMiddleInitialLastName(s)
          stu_user = ''.join(x[0] for x in self.NONLETTERS_PATTERN.split(name_tokens[1]) if len(x) > 0) + ''.join(x for x in self.NONLETTERS_PATTERN.split(name_tokens[0]))
          if len(stu_user) > 15:
            stu_user = stu_user[:15]
          ret[class_id].append({'username': stu_user, 'name': stu_name, 'id': stu_id, 'email': stu_email, 'phone': stu_phone, 'sectionid': section_id})
        except:
          break
      # Done with this class; return to main menu
      self.browser.find_element_by_name('SUBMIT2').submit()
    return ret
  def get_add_codes(self):
    """
    Returns a dictionary of add codes info, where keys are class ids and values are lists of add codes
    """
    # Log in
    self.browser.get('https://wave.cabrillo.edu')
    self.browser.find_element_by_link_text('Log In').click()
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "USER_NAME")))
    user_name_field = self.browser.find_element_by_id('USER_NAME')
    while user_name_field.get_attribute('value') != self.username:
      user_name_field.clear()
      self.browser.execute_script('document.getElementById("USER_NAME").value = "%s"' % self.username)
    passphrase_field = self.browser.find_element_by_id('CURR_PWD')
    while passphrase_field.get_attribute('value') != self.passphrase:
      passphrase_field.clear()
      self.browser.execute_script('document.getElementById("CURR_PWD").value = "%s"' % self.passphrase)
    self.browser.find_element_by_id('USER_NAME').submit()
    # Faculty menu
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Faculty")))
    self.browser.find_element_by_link_text('Faculty').click()
    ret = dict()
    # For each section...
    for class_num in range(1, 20):
      WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Add Codes")))
      self.browser.find_element_by_link_text('Add Codes').click()
      WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "VAR1")))
      full_term_name = {'s': 'Spring', 'f': 'Fall'}[self.term[0]] + ' 20' + self.term[1:]
      self.browser.execute_script('''
        document.getElementById('VAR1').selectedIndex = 1;
        var dd = document.getElementById('VAR1');
        for (var i = 0; i < dd.options.length; i++) {
            if (dd.options[i].text === '%s') {
                dd.selectedIndex = i;
                break;
            }
        }
        ''' % full_term_name)
      self.browser.find_element_by_name('SUBMIT2').click()
      # Select the next section
      try:
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'LIST_VAR1_%d' % class_num)))
        self.browser.find_element_by_id('LIST_VAR1_%d' % class_num).click()
      except:
        break
      self.browser.find_element_by_name('SUBMIT2').click()
      WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'VAR1')))
      class_name = self.browser.find_element_by_id('VAR1').text # Here we use the full section text as a name...
      ret[class_name] =[]
      # All students
      for td in self.browser.find_elements_by_class_name('LIST_VAR7'):
        ret[class_name].append(td.text)
      # Done with this class; return to main menu
      self.browser.find_element_by_name('OK2').submit()
    return ret
  def __del__(self):
    self.browser.close()
    self.browser.quit()
