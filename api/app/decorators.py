from app.errors import bad_request
from flask import jsonify, request
from functools import wraps

def paginated_response(model_class, endpoint):
    def decorator(func):
        @wraps(func)
        def paginate(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            query, id = func(*args, **kwargs)
            data = model_class.to_collection_dict(query, page, per_page, endpoint, id=id)
            if page < 0:
                return bad_request('Page must be nonnegative')
            if data['_meta']['total_pages'] > 0 and \
                    (page <= 0 or page > data['_meta']['total_pages']):
                return bad_request('Page must be between 1 and total pages')
            if per_page < 1:
                return bad_request('Per page must be at least 1')
            return jsonify(data)
        return paginate
    return decorator