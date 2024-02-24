class UserAccountsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'useraccounts':
            return 'web_template'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name == 'useraccounts':
            return 'web_template'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.model_name == 'useraccounts' or \
           obj2._meta.model_name == 'useraccounts':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'web_template':
            return model_name == 'useraccounts'
        elif model_name == 'useraccounts':
            return False
        return None
