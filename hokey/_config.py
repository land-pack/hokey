class ConfigSample:
    PREFIX = ''
    MAIN_SPLIT = []
    MESSAGE_ID = 'message_id'
    DEVICE_ID = 'device_id'
    HOST = '127.0.0.1'
    PORT = 5555
    DEBUG = True
    ESCAPE_LIST = {}


class Config(dict):
    def from_object(self, obj):
        """Updates the values from the given object.  An object can be of one
        of the following two types:
        //-   a string: in this case the object with that name will be imported
        -   an actual object reference: that object is used directly
        Objects are usually either modules or classes.
        Just the uppercase variables in that object are stored in the config.
        Example usage::
        //    app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)
        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_pyfile` and ideally from a location not within the
        package because the package might be installed system wide.
        :param obj: an import name or object
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


class Hokey:
    config = Config()  # A extends Dict!


if __name__ == '__main__':
    p = Hokey()
    p.config.from_object(ConfigSample)  # This config method can be easy load!
    p.config['ak'] = 'kkkk'  # There also another config method
    print p.config
