from langchain_core.tools import tool
from pydantic import BaseModel, Field

from schema import OrderStatusRequest, ProductInfoRequest

@tool
def get_order_status(req: OrderStatusRequest) -> str:
    """Get the current status of the user's order."""
    fake_orders = {
        "order_1": "Shipped",
        "order_2": "Processing",
        "order_3": "Delivered"
    }
    return fake_orders.get(req.order_id, "Order not found.")

@tool
def get_product_info(req: ProductInfoRequest) -> str:
    """Get information about a product given its ID."""
    fake_info = {
        "123": "Product 123 is a high-quality widget.",
        "456": "Product 456 is an advanced gadget."
    }
    return fake_info.get(req.product_id, "Product not found.")

@tool
def get_all_products() -> str:
    """List all available products."""
    products = ["123", "456", "789"]
    return "Available products: " + ", ".join(products)

@tool
def get_warranty_policy() -> str:
    """Get the warranty policy for a given product."""
    return "All products come with a one-year warranty covering manufacturing defects."

tools = [get_order_status, get_all_products, get_product_info, get_warranty_policy]