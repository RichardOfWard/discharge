class Plugin(object):
    roles = ()

    def __init__(self):
        site = None

    def add_to_site(self, site):
        self.site = site
        for role in self.roles:
            self.register_role(role)

    def register_role(self, role):
        self.site.register_role(self, role)
