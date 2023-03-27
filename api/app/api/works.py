from app.api import bp

@bp.route('/works', methods=['GET'])
def get_works():
    pass

@bp.route('/works', methods=['POST'])
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

@bp.route('/prompters/<int:id>/works', methods=['GET'])
def get_prompter_works(id):
    pass

@bp.route('/works/<int:id>/likers', methods=['GET'])
def get_likers(id):
    pass