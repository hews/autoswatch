default_configuration = {
    'SECRET_KEY': 'notverysecret',
    'DEBUG':      True
}

test_configuration = {
     'DEBUG': False,
     'TEST':  True
}

def config_app(app):
    app.config.from_object(default_configuration)
    app.config.from_envvar("CONFIG_FILE", silent=True)


# From: https://damyanon.net/flask-series-configuration/
#
# Best Practice is to have a default configuration, which is under
# source control and to override it with sensitive and specific
# information kept in instance folders. For the default configuration
# you could use object-based configuration hierarchy (described in
# Object-based configuration section) and to manage which
# configuration object to load via environment variables:
#
# ```python
# config = {
#     "development": "bookshelf.config.DevelopmentConfig",
#     "testing": "bookshelf.config.TestingConfig",
#     "default": "bookshelf.config.DevelopmentConfig"
# }
#
# def configure_app(app):
#     config_name = os.getenv('FLASK_CONFIGURATION', 'default')
#     app.config.from_object(config[config_name]) # object-based default configuration
#     app.config.from_pyfile('config.cfg', silent=True) # instance-folders configuration
#
# ```

# Also:
#   http://exploreflask.com/en/latest/configuration.html

# From:  http://flask.pocoo.org/docs/0.12/config/
#
# Configuration Best Practices
#
# The downside with the approach mentioned earlier is that it makes
# testing a little harder. There is no single 100% solution for this
# problem in general, but there are a couple of things you can keep in
# mind to improve that experience:
#
# Create your application in a function and register blueprints on it.
# That way you can create multiple instances of your application with
# different configurations attached which makes unittesting a lot
# easier. You can use this to pass in configuration as needed.
#
# Do not write code that needs the configuration at import time. If you
# limit yourself to request-only accesses to the configuration you can
# reconfigure the object later on as needed.
