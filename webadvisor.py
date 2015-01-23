# WebAdvisor roster scraper
# Limitations: User can have no more than 20 sections and 100 students per section
# Author: Jeffrey Bergamini
import sys
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select

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
    self.browser.find_element_by_id('USER_NAME').send_keys(self.username)
    self.browser.find_element_by_id('CURR_PWD').send_keys(self.passphrase)
    self.browser.find_element_by_id('USER_NAME').submit()
    # Faculty menu
    self.browser.find_element_by_link_text('FACULTY: Click Here').click()
    ret = dict()
    # For each section...
    for class_num in range(1, 20):
      self.browser.find_element_by_link_text('Class Roster').click()
      Select(self.browser.find_element_by_id('VAR1')).select_by_index(1)
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
          ret[class_id].append({'username': stu_user, 'name': stu_name, 'id': stu_id, 'email': stu_email, 'phone': stu_phone})
        except:
          break
      # Done with this class; return to main menu
      self.browser.find_element_by_name('SUBMIT2').submit()
    return ret
  def __del__(self):
    self.browser.close()
    self.browser.quit()
