from app.api import bp

@bp.route('/works', method=['GET'])
def get_works():
    pass

@bp.route('/works', method=['POST'])
def create_work():
    pass

@bp.route('/works/<int:id>', methods=['GET'])
def get_work(id):
    pass

@bp.route('/works/<int:id>', methods=['PUT'])
def update_work(id):
    pass

@bp.route('/works/<int:id>', methods=['DELETE'])
def delete_work(id):
    pass