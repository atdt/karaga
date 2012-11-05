Karaga
======

Karaga is the a Selenium test runner for MediaWiki sites.

Setup
-----

To install, run:

```sh
$ pip install -e git+https://github.com/atdt/karaga.git#egg=karaga
```

Before you can use Karaga, you'll need to create the file `.karaga.cfg` in your
home directory:

```ini
# example .karaga.cfg file

[sauce]
user = saucy_hacker                         # sauce labs username
key = 73ac7051-e083-82f2-91bc-fe5273085a94  # sauce labs key
timeout = 30                                # per-action timeout in seconds (default: 30)
```

Understand
----------

Test cases inherit from `unittest.TestCase`. Each test case class should define
a `platform` member, specifying platform to test again (currently only
`firefox`) and optionally a `base_url` member, which will be prepended to
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

* `assertText(text, msg=None)`:

  Assert that `text` is present somewhere on the page

* `assertElementPresent(selector, msg=None)`

  Assert that one or more elements matching `selector` exists

* `assertDefined(varname)`

  Assert that a JavaScript global `varname` is defined

* `assertExpression(expr)`

  Asserts that JavaScript expression `expr` evaluates to true

* `assertCookie(name)`

  Asserts that a cookie named `name` is present

* `assertHtml(html)`

  Asserts that `html` is present in the page source

* `assertQuerySelector(selector)`

  Asserts $(`selector`) returns a nonempty set

* `assertQuerySelectorEmpty(selector)`

  Asserts $(`selector`) returns a nonempty set



Karaga also adds the following MediaWiki-specific assert methods:


* `assertModuleState(module, state)`

  Asserts that ResourceLoader module `module` has state `state` (e.g., `ready`,
  `loaded`, etc.)

* `assertNoModuleFailures(self)`

  Asserts that no ResourceLoader module reports state `error`.