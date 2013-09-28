class Plugin(object):
    def can_handle_file(self, site, path):
        return False

    def build_file(self, site, path):
        raise NotImplementedError(
            "%s.build_file not implemented" % self.__class__.__name__)

    def build_misc(self, site):
        pass
