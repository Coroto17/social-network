from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

# executable_path="/home/ecc/geckodriver/geckodriver"
class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["network/fixture/fixture.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def TestLogin(self):
        """ Test that an user can login """
        timeout = 10
        self.selenium.get(f"{self.live_server_url}/login")
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("ecc2")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("el pez que fuma")
        self.selenium.find_element_by_xpath("//input[@value='Login']").click()
        # Wait until the response is received
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id("ecc2")
        )
        el = self.selenium.find_element_by_id("ecc2")
        self.assertEqual(el.get_attribute("class"), "nav-link text-light")

    def TestLike(self):
        """ Test that an user can like posts """
        like_hearts = self.selenium.find_elements_by_css_selector(
            "i[class*='fa-heart']"
        )
        for heart in like_hearts:
            self.assertFalse("text-danger" in heart.get_attribute("class"))
        for heart in like_hearts:
            heart.click()
        sleep(2)
        for heart in like_hearts:
            self.assertTrue(
                "text-danger" in heart.get_attribute("class"),
                msg=f"{heart.get_attribute('class')}",
            )

    def test_login(self):
        """ Test that an user can login"""
        self.TestLogin()

    def test_login_then_like(self):
        """Test that an user can login and like"""
        self.TestLogin()
        sleep(3)
        self.TestLike()
