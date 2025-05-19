from .registry_manager import log_and_register

def auto_register(model_name):
    def decorator(train_fn):
        def wrapper(*args, **kwargs):
            model, params, metrics = train_fn(*args, **kwargs)
            return log_and_register(model, params, metrics, model_name)
        return wrapper
    return decorator
