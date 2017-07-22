from textwrap   import dedent
from tempfile   import NamedTemporaryFile
from contextlib import contextmanager

import autoswatch

from flask import Flask
from nose.tools import (
    assert_equals,
    assert_true,
    assert_false
)

class TestApp:
    """
    The unit tests are for the basic structure of the app,
    its configuration (and environments), and that it starts up
    and runs when the container is created.
    """

    def test_create_app_returns_app(self):
        """
        Assert that create_app returns an app.
        """
        app = autoswatch.create_app()
        assert_true(isinstance(app, Flask))

    def test_default_config_debug(self):
        """
        Assert that create_app, by default, runs in debug mode.
        """
        app = autoswatch.create_app({})
        assert_true(app.debug)

    def test_env_dev_config(self):
        """
        Assert when ENV is set to development it loads that config.
        """
        config = autoswatch.env_config('development')
        app    = autoswatch.create_app(config)
        assert_true(app.debug)

    def test_env_test_config(self):
        """
        Assert when ENV is set to test or test-guard it loads that config.
        """
        config = autoswatch.env_config('test')
        app    = autoswatch.create_app(config)

        assert_false(app.debug)
        assert_true(app.testing)

    def test_env_test_guard_config(self):
        """
        Assert when ENV is set to test or test-guard it loads that config.
        """
        config = autoswatch.env_config('test-guard')
        app    = autoswatch.create_app(config)

        assert_false(app.debug)
        assert_true(app.testing)

    def test_env_prod_config(self):
        """
        Assert when ENV is set to production it loads that config.
        """
        config = autoswatch.env_config('production')
        app    = autoswatch.create_app(config)

        assert_false(app.debug)
        assert_false(app.config['JSONIFY_PRETTYPRINT_REGULAR'])

    @contextmanager
    def config_file(self, contents):
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(bytes(dedent(contents).encode('utf-8')))
            tmpfile.seek(0)
            yield dict(path=tmpfile.name, pointer=tmpfile)

    def test_instance_config_loads(self):
        """
        Assert that given an instance file it is loaded into config.
        """
        contents = """
          SECRET_KEY="stillnottoosecret"
        """
        with self.config_file(contents) as config_file:
            app = autoswatch.create_app({}, config_file['path'])
            assert_equals(app.config['SECRET_KEY'], 'stillnottoosecret')

    def test_instance_config_overrides(self):
        """
        Assert that an instance file overrides default and ENV configs.
        """
        contents = """
          SECRET_KEY="stillnottoosecret"
        """
        with self.config_file(contents) as config_file:
            env_config = {
                'SECRET_KEY': 'somewhatsecret'
            }
            app = autoswatch.create_app(env_config, config_file['path'])
            assert_equals(app.config['SECRET_KEY'], 'stillnottoosecret')
