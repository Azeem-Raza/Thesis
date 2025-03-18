import os
from typing import Dict, List, Tuple, Any, Optional, Annotated, TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from data import products, orders

# Load environment variables
load_dotenv()

# Initialize the Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192"
)

# Define the state for our graph
class AgentState(TypedDict):
    """Represents the state of our agent throughout the interaction."""
    user_input: str
    product_info: Optional[List[Dict]]
    order_info: Optional[Dict]
    response: Optional[str]

def should_retrieve_product_info(state: AgentState) -> Dict[str, str]:
    """Determine if we need to retrieve product information based on user input."""
    # Using the LLM to decide if this is a product-related query
    prompt = ChatPromptTemplate.from_template(
        """Determine if the following customer query is asking about a specific mobile phone product.
        
        Customer query: {query}
        
        If the customer is asking about a specific phone, its availability, price, features, etc., 
        respond with "RETRIEVE_PRODUCT".
        
        If the customer is asking about an order status or anything related to an order, 
        respond with "NO".
        
        If the query is not about a specific product or is a general greeting or question, 
        respond with "NO".
        
        Respond with just "RETRIEVE_PRODUCT" or "NO"."""
    )
    
    chain = prompt | llm
    result = chain.invoke({"query": state["user_input"]}).content.strip()
    
    if "RETRIEVE_PRODUCT" in result:
        return {"next": "retrieve_product"}
    else:
        return {"next": "next_step"}

def should_retrieve_order_info(state: AgentState) -> Dict[str, str]:
    """Determine if we need to retrieve order information based on user input."""
    # Using the LLM to decide if this is an order-related query
    prompt = ChatPromptTemplate.from_template(
        """Determine if the following customer query is asking about a specific order.
        
        Customer query: {query}
        
        If the customer is asking about an order status, tracking information, or mentions an order number,
        respond with "RETRIEVE_ORDER".
        
        If the query is not about an order, respond with "NO".
        
        Respond with just "RETRIEVE_ORDER" or "NO"."""
    )
    
    chain = prompt | llm
    result = chain.invoke({"query": state["user_input"]}).content.strip()
    
    if "RETRIEVE_ORDER" in result:
        return {"next": "retrieve_order"}
    else:
        return {"next": "generate_response"}

def retrieve_product_info(state: AgentState) -> AgentState:
    """Extract product name from query and retrieve product information."""
    # Using the LLM to extract the product name
    product_extract_prompt = ChatPromptTemplate.from_template(
        """Extract the mobile phone product name or description from the following customer query.
        Only extract the product name or type that the customer is asking about.
        
        Customer query: {query}
        
        For example:
        - If query is "Do you have iPhone 15 Pro in stock?", output "iPhone 15 Pro"
        - If query is "Is the Samsung Galaxy S24 Ultra available?", output "Samsung Galaxy S24 Ultra"
        - If query is "Tell me about Google Pixel phones", output "Google Pixel"
        
        Output just the product name or product type, nothing else."""
    )
    
    chain = product_extract_prompt | llm
    product_name = chain.invoke({"query": state["user_input"]}).content.strip()
    
    # Search for the product in our inventory
    matched_products = []
    for product in products:
        # Check if product name is in the product's name or brand
        if (product_name.lower() in product["name"].lower() or 
            product_name.lower() in product["brand"].lower()):
            matched_products.append(product)
    
    # Update state with product info
    new_state = state.copy()
    new_state["product_info"] = matched_products if matched_products else None
    return new_state

def retrieve_order_info(state: AgentState) -> AgentState:
    """Extract order number from query and retrieve order information."""
    # Using the LLM to extract the order number
    order_extract_prompt = ChatPromptTemplate.from_template(
        """Extract the order number from the following customer query.
        Only extract the order number that the customer is asking about.
        
        Customer query: {query}
        
        For example:
        - If query is "What's the status of order ORD10001?", output "ORD10001"
        - If query is "When will my order #ORD10003 arrive?", output "ORD10003"
        - If query is "I want to know about order number ORD10002", output "ORD10002"
        
        Output just the order number, nothing else. If no specific order number is mentioned, output "NO_ORDER_NUMBER"."""
    )
    
    chain = order_extract_prompt | llm
    order_number = chain.invoke({"query": state["user_input"]}).content.strip()
    
    new_state = state.copy()
    
    if order_number == "NO_ORDER_NUMBER":
        new_state["order_info"] = None
        return new_state
    
    # Search for the order in our database
    matched_order = None
    for order in orders:
        if order["order_id"] == order_number:
            matched_order = order.copy()
            # Add product details to the order
            for product in products:
                if product["id"] == order["product_id"]:
                    matched_order["product_details"] = product
                    break
            break
    
    # Update state with order info
    new_state["order_info"] = matched_order
    return new_state

def generate_response(state: AgentState) -> AgentState:
    """Generate a response based on the current state."""
    new_state = state.copy()
    
    if state.get("product_info"):
        product_info_str = ""
        product_info = state["product_info"]
        
        if not product_info:  # No products found
            response_prompt = ChatPromptTemplate.from_template(
                """You are a helpful customer service agent for a mobile phone retailer.
                The customer asked: "{query}"
                
                We don't have any products matching their description in our inventory.
                
                Provide a helpful response informing them that we don't have the product they're looking for.
                Suggest they check out other phones we have available and mention a couple of alternatives from our inventory.
                Be polite and professional."""
            )
            
            chain = response_prompt | llm
            response = chain.invoke({
                "query": state["user_input"]
            }).content
            
        elif len(product_info) == 1:  # Single product match
            product = product_info[0]
            availability = "In Stock" if product["stock"] > 0 else "Out of Stock"
            
            response_prompt = ChatPromptTemplate.from_template(
                """You are a helpful customer service agent for a mobile phone retailer.
                The customer asked: "{query}"
                
                We have the following product that matches their query:
                - Name: {name}
                - Brand: {brand}
                - Price: ${price}
                - Availability: {availability} ({stock} units)
                - Description: {description}
                - Specifications: {specs}
                
                Provide a helpful response addressing their query about this product.
                If they're asking about availability and the product is out of stock, apologize and suggest when it might be back in stock.
                Be polite, professional, and stick to the facts about the product. 
                DO NOT make up information not provided above."""
            )
            
            chain = response_prompt | llm
            response = chain.invoke({
                "query": state["user_input"],
                "name": product["name"],
                "brand": product["brand"],
                "price": product["price"],
                "availability": availability,
                "stock": product["stock"],
                "description": product["description"],
                "specs": str(product["specs"])
            }).content
            
        else:  # Multiple product matches
            for product in product_info:
                availability = "In Stock" if product["stock"] > 0 else "Out of Stock"
                product_info_str += f"- {product['name']} ({product['brand']}): ${product['price']}, {availability} ({product['stock']} units)\n"
            
            response_prompt = ChatPromptTemplate.from_template(
                """You are a helpful customer service agent for a mobile phone retailer.
                The customer asked: "{query}"
                
                We have several products that match their query:
                {product_info}
                
                Provide a helpful response addressing their query about these products.
                If they're asking about a specific one, focus on that one.
                If they're asking generally, give an overview of the options.
                Be polite, professional, and stick to the facts about the products.
                DO NOT make up information not provided above."""
            )
            
            chain = response_prompt | llm
            response = chain.invoke({
                "query": state["user_input"],
                "product_info": product_info_str
            }).content
    
    elif state.get("order_info"):
        # Generate response about the order
        order = state["order_info"]
        product_details = order.get("product_details", {})
        
        response_prompt = ChatPromptTemplate.from_template(
            """You are a helpful customer service agent for a mobile phone retailer.
            The customer asked: "{query}"
            
            We found the following order information:
            - Order ID: {order_id}
            - Customer: {customer_name}
            - Product: {product_name} ({product_id})
            - Quantity: {quantity}
            - Status: {status}
            - Order Date: {order_date}
            - Shipping Address: {shipping_address}
            - Tracking Number: {tracking_number}
            
            Provide a helpful response addressing their query about this order.
            Be polite, professional, and stick to the facts about the order.
            DO NOT make up information not provided above."""
        )
        
        chain = response_prompt | llm
        response = chain.invoke({
            "query": state["user_input"],
            "order_id": order["order_id"],
            "customer_name": order["customer_name"],
            "product_name": product_details.get("name", "Unknown product"),
            "product_id": order["product_id"],
            "quantity": order["quantity"],
            "status": order["status"],
            "order_date": order["order_date"],
            "shipping_address": order["shipping_address"],
            "tracking_number": order["tracking_number"] if order["tracking_number"] else "Not available"
        }).content
    
    else:
        # General response for queries that don't match products or orders
        response_prompt = ChatPromptTemplate.from_template(
            """You are a helpful customer service agent for a mobile phone retailer.
            The customer asked: "{query}"
            
            We couldn't find specific product or order information related to their query.
            
            Provide a helpful general response. If they're asking about products or services we offer,
            give them general information about our mobile phone retail business.
            
            Be polite and professional. Ask clarifying questions if needed.
            DO NOT make up specific products or prices."""
        )
        
        chain = response_prompt | llm
        response = chain.invoke({
            "query": state["user_input"]
        }).content
    
    new_state["response"] = response
    return new_state

# Create and define the graph
def build_graph():
    # Define state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("check_product", should_retrieve_product_info)
    workflow.add_node("retrieve_product", retrieve_product_info)
    workflow.add_node("check_order", should_retrieve_order_info)
    workflow.add_node("retrieve_order", retrieve_order_info)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("next_step", lambda x: x)  # Pass-through node
    
    # Set the entry point
    workflow.set_entry_point("check_product")
    
    # Add edges using conditional_edges for router nodes
    workflow.add_conditional_edges(
        "check_product",
        lambda x: x.get("next", "next_step"),
        {
            "retrieve_product": "retrieve_product",
            "next_step": "next_step"
        }
    )
    
    workflow.add_edge("retrieve_product", "next_step")
    workflow.add_edge("next_step", "check_order")
    
    workflow.add_conditional_edges(
        "check_order",
        lambda x: x.get("next", "generate_response"),
        {
            "retrieve_order": "retrieve_order",
            "generate_response": "generate_response"
        }
    )
    
    workflow.add_edge("retrieve_order", "generate_response")
    workflow.add_edge("generate_response", END)
    
    return workflow.compile()

# Build the graph
customer_support_agent = build_graph()

def process_query(user_input: str) -> str:
    """Process a user query and return the agent's response."""
    # Initialize state with user input
    initial_state = {"user_input": user_input, "product_info": None, "order_info": None, "response": None}
    
    # Run the graph
    result = customer_support_agent.invoke(initial_state)
    
    # Return the response
    return result["response"]

if __name__ == "__main__":
    # Test the agent
    test_query = "Do you have the iPhone 15 Pro in stock?"
    response = process_query(test_query)
    print(f"Query: {test_query}")
    print(f"Response: {response}") 