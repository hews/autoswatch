import autoswatch

from nose.tools import assert_equals

class TestApp:
    """
    The unit tests are for the basic structure of the app,
    its configuration (and environments), and that it starts up
    and runs when the container is created.
    """
    pass

    # ##################################################################
    # TODO: test for…
    #   - create_app returns an app
    #   - by default debug is on
    #   - given environment of:
    #     - development it has settings…,
    #     - test/test-guard it has settings…,
    #     - production it has settings…
    #   - given an instance/config.py file:
    #     - it is loaded into settings,
    #     - it overrides default and environment settings.
    #

