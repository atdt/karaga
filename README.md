Karaga
======

Karaga is a [Sauce Labs](http://saucelabs.com/) Selenium test runner for
[MediaWiki](http://www.mediawiki.org/) sites. Karaga subclasses the `TestCase`
class from Python's [unittest](http://docs.python.org/library/unittest.html),
adding assert methods based on common web testing patterns, such as checking
for the presence of some element on the page, or checking that a cookie has
been set.

Setup
-----
_Note: A [Sauce Labs](http://saucelabs.com) account is required._

To install, run:

```sh
$ pip install -e git+https://github.com/atdt/karaga.git#egg=karaga
```

Before you can use Karaga, you'll need to create the file `.karaga.cfg` in your
home directory:

```ini
# example .karaga.cfg file

[sauce]
user = saucy_hacker
key = 73ac7051-e083-82f2-91bc-fe5273085a94
```

Understand
----------

Test cases inherit from `unittest.TestCase`. Each test case class should define
a `platform` member, specifying platform to test again (currently only
firefox) and optionally a `base_url` member, which will be prepended to
every URL requested in the tests.

```python
class MyTestCase(karaga.MediaWikiTestCase):
    platform = 'firefox'
    base_url = 'http://wiki.karaga.org/w/'
```

The Selenium driver is accessible from within tests as `self.browser`. For
convenience, calling `self.get(url)` opens the page at `url`, prepended by
`self.base_url` (if the class defines it).

```python
  def test_page_load(self):
      """Retrieves /home.html and ensures 'Welcome' is in the document text"""
      self.get('/home.html')
      self.assertText('Welcome')
```

In addition to unittest's set of assert methods, Karaga adds the following
generic asserts:

```python
assertText(text, msg=None)
# Assert that text is present somewhere on the page

assertElementPresent(selector, msg=None)
# Assert that one or more elements matching selector exists

assertDefined(varname)
# Assert that a JavaScript global varname is defined

assertExpression(expr)
# Asserts that JavaScript expression expr evaluates to true

assertCookie(name)
# Asserts that a cookie named name is present

assertHtml(html)
# Asserts that html is present in the page source

assertQuerySelector(selector)
# Asserts $(selector) returns a nonempty set

assertQuerySelectorEmpty(selector)
# Asserts $(selector) returns a nonempty set
```


Karaga also adds the following MediaWiki-specific assert methods:


```python
assertModuleState(module, state)
# Asserts that ResourceLoader module module has state state (e.g., ready, loaded, etc.)

assertNoModuleFailures(self)
# Asserts that no ResourceLoader module reports state error.
```
