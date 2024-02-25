class Cart():
 
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get('session_key')
        
        if 'session.key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart
    
    def add(self, product):
        product_id = str(product.id)
        print("Hello")
        if product_id in self.cart:
            pass
        else:
            if product.is_sale:
                self.cart[product_id] = {'price':str(product.sale_price)}
            else:
                self.cart[product_id] = {'price':str(product.price)}
        
        self.session.modified = True