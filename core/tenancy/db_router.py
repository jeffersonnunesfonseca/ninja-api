import threading

_thread_locals = threading.local()


def set_current_tenant(alias):
    _thread_locals.tenant = alias


def get_current_tenant():
    return getattr(_thread_locals, "tenant", "default")


class MultiTenantRouter:
    def db_for_read(self, model, **hints):
        return get_current_tenant()

    def db_for_write(self, model, **hints):
        return get_current_tenant()
