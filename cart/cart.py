from store.models import Product


class Cart():
 
    def __init__(self, request) -> None:
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            # cart = self.session['session_key'] = {}
            cart = self.session['session_key'] = {}

        self.cart = cart
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(quantity)
            # self.cart[product_id] = {'price':str(product.price)}
            # self.cart[product_id] = {'price': str(product.price)}
        
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities