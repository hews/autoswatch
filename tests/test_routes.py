import autoswatch

from autoswatch.utils import captured_templates

from nose.tools import (
    assert_true,
    assert_in,
    assert_equals,
    with_setup
)

class TestRoutes:
    """
    These unit tests are for the basic API of the app's routes.

    If we add functional tests we'll run them separately under /e2e.
    """

    @classmethod
    def setup_class(self):
        self.app    = autoswatch.app
        self.client = self.app.test_client()

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
        Assert that the app renders custom error handlers
        for a 404 error.
        """
        templates = []
        with captured_templates(self.app, templates):
            res = self.app.test_client().get('/path/does/not/exist')
            template, context = templates[0]
            assert_equals(template.name, '404.j2')

    def test_400_route(self):
        """
        Assert that the app renders custom error handlers
        for a 400 error.
        """
        templates = []
        with captured_templates(self.app, templates):
            res = self.app.test_client().get('/hex/notahexval')
            template, context = templates[0]
            assert_equals(template.name, '400.j2')

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
