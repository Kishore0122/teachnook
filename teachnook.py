from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
import json

# Define a Product with essential details
@dataclass
class Product:
    name: str
    description: str
    price: Decimal
    product_id: str
    stock: int = 0
    category: str = "Uncategorized"

    # Convert product details to a dictionary format for easy JSON export
    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "category": self.category
        }

# Define a Service with necessary details
@dataclass
class Service:
    name: str
    description: str
    duration: int  # in minutes
    price: Decimal
    service_id: str
    available_slots: List[str] = field(default_factory=list)
    category: str = "Uncategorized"

    # Convert service details to a dictionary format for easy JSON export
    def to_dict(self) -> dict:
        return {
            "service_id": self.service_id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "price": float(self.price),
            "category": self.category,
            "available_slots": self.available_slots
        }

# Manage stock levels of products
class InventoryManagement:
    def add_stock(self, product: Product, quantity: int) -> None:
        """Adds stock to the specified product."""
        if product:
            product.stock += quantity
            print(f"Added {quantity} to stock of '{product.name}'. New stock: {product.stock}")

    def remove_stock(self, product: Product, quantity: int) -> bool:
        """Removes stock from the specified product if sufficient stock is available."""
        if product and product.stock >= quantity:
            product.stock -= quantity
            print(f"Removed {quantity} from stock of '{product.name}'. New stock: {product.stock}")
            return True
        print(f"Failed to remove stock. Not enough stock for '{product.name}'.")
        return False

# Main application to manage products and services
class Application:
    def __init__(self):
        self.products: List[Product] = []
        self.services: List[Service] = []
        self.inventory = InventoryManagement()

    def add_product(self, product: Product) -> None:
        """Adds a new product to the inventory."""
        self.products.append(product)
        print(f"Product '{product.name}' added successfully.")

    def add_service(self, service: Service) -> None:
        """Adds a new service to the catalog."""
        self.services.append(service)
        print(f"Service '{service.name}' added successfully.")

    def find_product(self, product_id: str) -> Optional[Product]:
        """Finds and returns a product by its ID."""
        return next((p for p in self.products if p.product_id == product_id), None)

    def find_service(self, service_id: str) -> Optional[Service]:
        """Finds and returns a service by its ID."""
        return next((s for s in self.services if s.service_id == service_id), None)

    def update_product(self, product_id: str, **kwargs) -> bool:
        """Updates product details."""
        product = self.find_product(product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            print(f"Product '{product_id}' updated successfully.")
            return True
        print(f"Product '{product_id}' not found.")
        return False

    def update_service(self, service_id: str, **kwargs) -> bool:
        """Updates service details."""
        service = self.find_service(service_id)
        if service:
            for key, value in kwargs.items():
                if hasattr(service, key):
                    setattr(service, key, value)
            print(f"Service '{service_id}' updated successfully.")
            return True
        print(f"Service '{service_id}' not found.")
        return False

    def display_products(self, category: Optional[str] = None) -> None:
        """Displays all products or filters by category."""
        products = self.products
        if category:
            products = [p for p in products if p.category == category]

        print("\n=== Available Products ===")
        if not products:
            print("No products available.")
            return
        for idx, product in enumerate(products, 1):
            print(f"{idx}. {product.name} - {product.description}")
            print(f"   Price: ${float(product.price):.2f}")
            print(f"   Stock: {product.stock}")
            print(f"   Category: {product.category}")
            print(f"   ID: {product.product_id}\n")

    def display_services(self, category: Optional[str] = None) -> None:
        """Displays all services or filters by category."""
        services = self.services
        if category:
            services = [s for s in services if s.category == category]

        print("\n=== Available Services ===")
        if not services:
            print("No services available.")
            return
        for idx, service in enumerate(services, 1):
            print(f"{idx}. {service.name} - {service.description}")
            print(f"   Duration: {service.duration} mins")
            print(f"   Price: ${float(service.price):.2f}")
            print(f"   Category: {service.category}")
            if service.available_slots:
                print(f"   Next available slot: {service.available_slots[0]}\n")
            else:
                print("   No available slots\n")

    def export_catalog(self, filename: str) -> None:
        """Exports the catalog to a JSON file."""
        catalog = {
            "products": [p.to_dict() for p in self.products],
            "services": [s.to_dict() for s in self.services]
        }
        with open(filename, 'w') as f:
            json.dump(catalog, f, indent=2)
        print(f"Catalog exported to '{filename}' successfully.")

# Main function to demonstrate usage
def main():
    app = Application()

    # Sample products to add
    products = [
        Product("Premium Coffee Maker", "High-end automatic coffee machine", Decimal("299.99"), "P001", 10, "Appliances"),
        Product("Organic Coffee Beans", "Premium arabica beans, 1kg", Decimal("24.99"), "P002", 50, "Food"),
        Product("Coffee Filter Pack", "Pack of 100 paper filters", Decimal("9.99"), "P003", 200, "Accessories")
    ]

    for product in products:
        app.add_product(product)

    # Sample services to add
    services = [
        Service("Barista Training", "Learn coffee making fundamentals", 120, Decimal("149.99"), "S001", 
                ["2024-10-27 10:00", "2024-10-28 14:00"], "Education"),
        Service("Machine Maintenance", "Professional coffee machine cleaning", 60, Decimal("79.99"), "S002", 
                ["2024-10-27 09:00", "2024-10-27 15:00"], "Maintenance"),
        Service("Coffee Tasting", "Guided tasting of premium coffees", 90, Decimal("39.99"), "S003", 
                ["2024-10-29 11:00", "2024-10-30 11:00"], "Experience")
    ]

    for service in services:
        app.add_service(service)

    # Display products and services
    app.display_products()
    app.display_services()

    # Export catalog to JSON
    app.export_catalog("catalog.json")

    # Update product stock and price
    app.inventory.add_stock(app.find_product("P001"), 5)
    app.update_product("P002", price=Decimal("22.99"))

    print("\n=== After Updates ===")
    app.display_products()

if __name__ == "__main__":
    main()
