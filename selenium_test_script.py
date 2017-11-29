import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import re




class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)


    # Test Login
    def test_login(self):
        driver = self.driver
        driver.get('http://web:8000/login/')

        # find form fields and login button
        email = driver.find_element_by_id("id_email")
        password = driver.find_element_by_id("id_password")
        submit = driver.find_element_by_id("id_login")

        # enter user information
        email.send_keys("dan@kramp.com")
        password.send_keys("memes")

        # submit
        submit.send_keys(Keys.RETURN)

        # verify that "Logout" is on page (user is logged in)
        src = driver.page_source
        text_found = re.search(r'Logout', src)
        value = self.assertNotEqual(text_found, None)

    # Test Create Account
    def test_create_account(self):
        driver = self.driver
        driver.get('http://web:8000/register/')

        # find form fields
        email = driver.find_element_by_name("email")
        password = driver.find_element_by_name("password")
        f_name = driver.find_element_by_name("first_name")
        l_name = driver.find_element_by_name("last_name")
        register = driver.find_element_by_id("id_register")

        # enter user information
        email.send_keys("hello5@gmail.com")
        password.send_keys("password")
        f_name.send_keys("first1")
        l_name.send_keys("last1")

        # register
        register.send_keys(Keys.RETURN)

        # login
        login_email = driver.find_element_by_id("id_email")
        login_password = driver.find_element_by_id("id_password")
        submit = driver.find_element_by_id("id_login")
        login_email.send_keys("hello5@gmail.com")
        login_password.send_keys("password")
        submit.send_keys(Keys.RETURN)

        # verify that "Logout" is on page (user is logged in)
        src = driver.page_source
        text_found = re.search(r'Logout', src)
        self.assertNotEqual(text_found, None)

    def test_create_meal(self):
        driver = self.driver
        driver.get('http://web:8000/login/')

        # login
        email = driver.find_element_by_id("id_email")
        password = driver.find_element_by_id("id_password")
        submit = driver.find_element_by_id("id_login")
        email.send_keys("dan@kramp.com")
        password.send_keys("memes")
        submit.send_keys(Keys.RETURN)

        # go to create meal page
        create_meal = driver.find_element_by_id("id_create_meal")
        create_meal.send_keys(Keys.RETURN)

        # find fields
        meal_name = driver.find_element_by_id("id_name")
        meal_price = driver.find_element_by_id("id_price")
        meal_description = driver.find_element_by_id("id_description")
        meal_portions = driver.find_element_by_id("id_portions")
        create_button = driver.find_element_by_id("id_create")

        # sample meal
        meal_name.send_keys("Butter Chicken")
        meal_price.send_keys("100")
        meal_description.send_keys("Some Saucy Chicken")
        meal_portions.send_keys("10")

        create_button.send_keys(Keys.RETURN)

        src = driver.page_source
        text_found = re.search(r'Your meal was created.', src)
        value = self.assertNotEqual(text_found, None)

    def test_search_meal(self):
        driver = self.driver
        driver.get('http://web:8000/login/')

        # find form fields and login button
        email = driver.find_element_by_id("id_email")
        password = driver.find_element_by_id("id_password")
        submit = driver.find_element_by_id("id_login")

        # enter user information
        email.send_keys("dan@kramp.com")
        password.send_keys("memes")

        # login
        submit.send_keys(Keys.RETURN)

        # find search page button
        search = driver.find_element_by_id("id_Search")

        # go to search page
        search.send_keys(Keys.RETURN)

        # find search field and search button
        search_field = driver.find_element_by_id("id_q")
        small_search = driver.find_element_by_id("id_search_small")


        # enter search word and complete search
        search_field.send_keys("Hamburger")
        small_search.send_keys(Keys.RETURN)

        # check if search word exists on page
        src = driver.page_source
        text_found = re.search(r'Try searching for something!', src)
        self.assertEqual(text_found, None)








    # def tearDown(self):
    #     self.driver.close()





        # response = self.client.post(url, user_data, format='json')
        #
        # # Verify that it returns the desired status code
        # self.assertEqual(response.status_code, 200)
        #
        # # Verify still just one user in db
        # self.assertEqual(User.objects.count(), 1)
        #
        # # Compare email addresses to make sure they changed
        # self.assertEqual(User.objects.get(pk=self.first_user.id).email, 'testemail@test.net')

    # def test_search_in_python_org(self):
    #     driver = self.driver
    #     driver.get("http://www.python.org")
    #     self.assertIn("Python", driver.title)
    #     elem = driver.find_element_by_name("q")
    #     elem.send_keys("pycon")
    #     elem.send_keys(Keys.RETURN)
    #     assert "No results found." not in driver.page_source





if __name__ == "__main__":
    unittest.main()
