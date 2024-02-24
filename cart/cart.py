class Cart():
 
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get('session_key')
        
        if 'session.key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart