import autoswatch

from nose.tools import assert_true, assert_in, assert_equals, with_setup

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

    def test_root_route(self):
        """
        Assert that the app returns HTML from the root route.
        """
        res = self.client.get('/')
        assert_in('text/html', res.headers['Content-Type'])
        assert_true(len(res.get_data()) > 0)

    def test_404_route(self):
        """
        Assert that the app returns HTML from a 404 error.
        """
        res = self.client.get('/path/does/not/exist')
        assert_in('text/html', res.headers['Content-Type'])
        assert_true(len(res.get_data()) > 0)

    def test_400_route(self):
        """
        Assert that the app returns HTML from a 400 error.
        """
        res = self.client.get('/hex/notahexval')
        assert_in('text/html', res.headers['Content-Type'])
        assert_true(len(res.get_data()) > 0)

    def test_404_status(self):
        """
        Assert that 404 error codes returns a 404 status code.
        """
        res = self.client.get('/path/does/not/exist')
        assert_equals(res.status_code, 404)

    def test_400_status(self):
        """
        Assert that 400 error codes returns a 400 status code.
        """
        res = self.client.get('/hex/notahexval')
        assert_equals(res.status_code, 400)

    def test_hex_route_six_digit(self):
        """
        Assert that requests to /hex/hex_color are valid.
        """
        res = self.client.get('/hex/ff00aa')
        assert_equals(res.status_code, 200)
        assert_in('image/png', res.headers['Content-Type'])

    def test_hex_route_three_digit(self):
        """
        Assert that requests to /hex/hex_color are valid with 3-digit codes.
        """
        res = self.client.get('/hex/fff')
        assert_equals(res.status_code, 200)
        assert_in('image/png', res.headers['Content-Type'])

    def test_hex_route_with_octothorpe(self):
        """
        Assert that requests to /hex/hex_color are valid when include octothorpe.
        """
        res = self.client.get('/hex/%23b1b1b1')
        assert_equals(res.status_code, 200)
        assert_in('image/png', res.headers['Content-Type'])


    # ##################################################################
    # TODO: test for…
    #   - app environments
    #   - /<named_color> represents an html named color code
