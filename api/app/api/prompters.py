from app.api import bp

@bp.route('/prompters', methods=['GET'])
def get_prompters():
    pass

@bp.route('/prompters', methods=['POST'])
def create_prompter():
    pass

@bp.route('/prompters/<int:id>', methods=['GET'])
def get_prompter(id):
    pass

@bp.route('/prompters/<int:id>', methods=['PUT'])
def update_prompter(id):
    pass

@bp.route('/prompters/<int:id>/works', methods=['GET'])
def get_works(id):
    pass

@bp.route('/prompters/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass

@bp.route('/prompters/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass

@bp.route('/prompters/<int:id>/followed', methods=['POST'])
def follow(id):
    pass

@bp.route('/prompters/<int:follower_id>/followed/<int:followed_id>', methods=['DELETE'])
def unfollow(follower_id, followed_id):
    pass

@bp.route('/prompters/<int:id>/liked', methods=['GET'])
def get_liked(id):
    pass

@bp.route('/prompters/<int:id>/liked', methods=['POST'])
def like(id):
    pass

@bp.route('/prompters/<int:liker_id>/liked/<int:liked_id>', methods=['DELETE'])
def unlike(liker_id, liked_id):
    pass

@bp.route('/prompters/<int:id>/feed', methods=['GET'])
def feed(id):
    pass
