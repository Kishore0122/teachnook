class Product:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price
class Service:
    def __init__(self, name, description, duration, price):
        self.name = name
        self.description = description
        self.duration = duration
        self.price = price
class Application:
    def __init__(self):
        self.products = []
        self.services = []
    def add_product(self, product):
        self.products.append(product)
    def add_service(self, service):
        self.services.append(service)
    def display_products(self):
        print("Available Products:")
        for idx, product in enumerate(self.products, 1):
            print(f"{idx}. {product.name} - {product.description} - ${product.price}")
    def display_services(self):
        print("Available Services:")
        for idx, service in enumerate(self.services, 1):
            print(f"{idx}. {service.name} - {service.description} - Duration: {service.duration} mins - ${service.price}")
if __name__ == "__main__":
    app = Application()
    # Adding products
    app.add_product(Product("Product 1", "Description of Product 1", 10.0))
    app.add_product(Product("Product 2", "Description of Product 2", 20.0))
    # Adding services
    app.add_service(Service("Service 1", "Description of Service 1", 30, 50.0))
    app.add_service(Service("Service 2", "Description of Service 2", 60, 100.0))
    # Display products and services
    app.display_products()
    print("\n")
    app.display_services()
