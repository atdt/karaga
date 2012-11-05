# -*- coding: utf-8 -*-
import ConfigParser
import logging
import os
import sys
import unittest
import urlparse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


logging.basicConfig(stream=sys.stderr)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.karaga.cfg'))
sauce = dict(config.items('sauce'))


platforms = {
    'firefox': {
        'desired_capabilities': webdriver.DesiredCapabilities.FIREFOX,
    }
}


defaults = {
    'command_executor': "http://%(user)s:%(key)s@ondemand.saucelabs.com:80/wd/hub" % sauce
}


main = unittest.main


class Browser(webdriver.Remote):
    """
    Represents a remote WebDriver instance on our Mac Mini. Usage:

        >>> with Browser('Firefox') as browser:
        ...     browser.get('http://en.wikipedia.org/')
        ...     assert 'Wikipedia' in browser.title

    """

    def __init__(self, platform):
        """
        Constructor; `platform` is a string specifying platform to test on.
        """
        platform = platform.lower()
        driver_config = dict(defaults)
        driver_config.update(platforms.get(platform, {}))
        super(Browser, self).__init__(**driver_config)

        # shortcuts
        self.eval = self.execute_script
        self.el = self.find_element_by_css_selector
        self.els = self.find_elements_by_css_selector

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.quit()
        except WebDriverException:
            pass

    def val(self, expr):
        return self.eval('return (%s);' % expr)




class BangaloreTestCase(unittest.TestCase):
    """
    Choose a platform by setting a platform class attribute.
    """

    platform = None
    base_url = ''

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser(cls.platform)
        cls.browser.implicitly_wait(sauce.get('timeout', 30))

    @classmethod
    def tearDownClass(cls):
        try:
            cls.browser.quit()
        except WebDriverException:
            pass
        finally:
            log.info('https://saucelabs.com/jobs/{.session_id}'.format(cls.browser))

    def setUp(self):
        self.browser.delete_all_cookies()

    def assertText(self, text, msg=None):
        """ Assert that `text` is present somewhere on the page """
        page = self.browser.find_element_by_tag_name('html')
        self.assertIn(text, page.text, msg)

    def assertElementPresent(self, selector, msg=None):
        """ Assert that one or more elements matching `selector` exists """
        els = self.browser.els(selector)
        self.assertGreater(len(els), 0, msg)

    def assertDefined(self, varname):
        """ Assert that a JavaScript global `varname` is defined """
        js = 'return typeof %s !== "undefined"' % varname
        self.assertTrue(self.browser.eval(js), '"%s" is undefined' % varname)

    def assertExpression(self, expr):
        """ Asserts that JavaScript expression `expr` evaluates to true """
        js = 'return !!({0})'.format(expr)
        self.assertTrue(self.browser.eval(js))

    def assertCookie(self, name):
        """ Asserts that a cookie named `name` is present """
        self.assertIsNotNone(self.browser.get_cookie(name))

    def assertHtml(self, html):
        """ Asserts that `html` is present in the page source """
        self.assertIn(html, self.browser.page_source)  # pylint: disable=E1101

    def assertQuerySelector(self, selector):
        """ Asserts $(`selector`) returns a nonempty set """
        matches = self.browser.val("$('%s').length" % selector)
        self.assertTrue(matches)

    def assertQuerySelectorEmpty(self, selector):
        """ Asserts $(`selector`) returns a nonempty set """
        matches = self.browser.val("$('%s').length" % selector)
        self.assertFalse(matches)

    def get(self, url):
        if self.base_url is not None:
            url = urlparse.urljoin(self.base_url, url)
        return self.browser.get(url)


class MediaWikiTestCase(BangaloreTestCase):

    def assertModuleState(self, module, state):
        self.assertExpression('mw.loader.getState(%s) === "%s"' % (module, state))

    def assertNoModuleFailures(self):
        self.assertExpression('mw.loader.getModuleNames().filter(function (module) { return mw.loader.getState(module) === "error"; }).length === false')
