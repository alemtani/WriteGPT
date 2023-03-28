from app.errors import bad_request
from flask import jsonify, request
from functools import wraps

def paginated_response(model_class, endpoint):
    def decorator(func):
        @wraps(func)
        def paginate(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            query = func(*args, **kwargs)
            data = model_class.to_collection_dict(query, page, per_page, endpoint)
            if page < 1 or page > data['_meta']['total_pages']:
                return bad_request('page must be between 1 and total_pages')
            if per_page < 1:
                return bad_request('per_page must be at least 1')
            return jsonify(data)
        return paginate
    return decorator