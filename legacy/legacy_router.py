class LegacyRouter:
    """
    A router to control all database operations on models in the legacy application.
    """

    route_app_labels = {"legacy"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read legacy models go to the 'legacy' database.
        """
        if model._meta.app_label in self.route_app_labels:
            return "legacy"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write legacy models go to the 'legacy' database.
        """
        if model._meta.app_label in self.route_app_labels:
            return "legacy"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Disallows relations if a model in the legacy app is involved.
        """
        if obj1._meta.app_label in self.route_app_labels and obj2._meta.app_label in self.route_app_labels:
            return True
        elif obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
            return False
        return None

    def allow_migrate(self, db, app_label, **hints):
        """
        Make sure the legacy app only appear in the 'legacy' database, and nothing else does.
        """
        if app_label in self.route_app_labels:
            return db == "legacy"
        elif db == "legacy":
            return False
        return None
