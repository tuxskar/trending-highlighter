def json_dates_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return str(obj)
