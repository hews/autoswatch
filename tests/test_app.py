import autoswatch

from nose.tools import assert_true, assert_in, with_setup

class TestApp:
    """
    These unit tests are for the basic structure of the app,
    its configuration (and environments), and that it starts up
    and runs when the container is created.

    For functional tests we'll run a separate series of that
    live under e2e.
    """

    @classmethod
    def setup_class(self):
        autoswatch.app.testing = True
        self.client = autoswatch.app.test_client()

    @classmethod
    def teardown_class(self): pass

    def test_root(self):
        """
        Assert that the app returns HTML from the root route.
        """
        res = self.client.get('/')
        assert_in('text/html', res.headers['Content-Type'])
        assert_true(len(res.get_data()) > 0)

    # TODO: test for…
    #   - root html properly includes links to current server
    #   - root html links to current favicon (create favicon)
    #   - app environments
    #   - 404 missing
    #   - 400 bad request
    #   - <hex_value> valid (3 or 6, all hex, w/ or w/o octothorpe)
    #   - <hex_value> represents an html named color code
