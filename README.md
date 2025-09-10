# llm-chat

Chat system powered by LLM, integrated with Postgres database and Ollama model.

## Installation & Requirements (Local Environment)

### Requirements
- Python >= 3.13
- Docker (Optional)
- Available ports: 8000 (API), 5432 (Postgres), 11434 (Ollama)

### Option 1: Install & Run with Docker Compose
1. Clone this repository.
2. Run in terminal:
	```powershell
	docker-compose up -d --build
	```
3. FastAPI API will be available at `http://localhost:8000`.

### Option 2: Install & Run with uv (Python)
1. Clone this repository.
2. Install [uv](https://github.com/astral-sh/uv):
	```powershell
	pip install uv
	```
3. Install dependencies:
	```powershell
    cd src
    uv venv
    .venv\Scripts\activate    # activate venv for windows
	uv sync
	```
4. Start Postgres and Ollama manually.
5. Run the FastAPI server:
	```powershell
    uv run main.py
	```

### Environment Configuration
Copy `.env.example` to `.env` in the root directory, then adjust the variables as needed:
```sh
PGUSER=postgres
PGPASSWORD=mypassword
PGDB=chat_history
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=
OPENAI_MODEL=qwen3:1.7b
```

## Database Design
- **Table:** `message_store`
  - Stores chat history per session.
  - Automatically created by the application at runtime.
  - **Column**:
    - id (Integer)
    - session_id (UUID),
    - message (Json),
    - created_at (Timezone)
    

## Libraries and Frameworks Used
  - UV
  - FastAPI
  - Uvicorn
  - Langchain
  - OpenAI
  - Pyscopg (Postgre)
  - Pydantic


## LLM Model Used

- **Ollama** with model: `qwen3:1.7b` or **OpenAI** model
- Configurable via environment variable.

### Note on Qwen Model and Function Calls

While the Ollama Qwen model (`qwen3:1.7b`) can be used for general chat, it is not recommended for function/tool calls (such as API or tool invocation) because its reliability and accuracy for structured function calling is limited compared to OpenAI models. Llama models may not consistently follow the required function call format, which can result in failed or incorrect tool executions.


**Recommendation:**
- For best results and a better user experience, especially for function/tool calls, use an OpenAI model (e.g., `gpt-4o-mini`). OpenAI models are more reliable in following structured formats and handling tool/function calls, making them suitable for production and advanced use cases.
- To use OpenAI, set the following in your `.env` file:
  ```sh
  OPENAI_API_KEY=your_openai_key
  OPENAI_BASE_URL=https://api.openai.com/v1
  OPENAI_MODEL=gpt-4o-mini
  ```
- Example requests and responses in this documentation use OpenAI for demonstration.

## Example Questions Answered
- Order status
- Product information
- List of available products
- Product warranty policy

## Available Tool Calls
- `get_order_status(order_id)`: Check order status.
- `get_product_info(product_id)`: Get product information.
- `get_all_products()`: List all products.
- `get_warranty_policy()`: Show warranty policy.

## Example Request & Response

### 1. Get Order Status
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "What is the status of my order 'order_1'?"
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "Your order 'order_1' status is: Shipped."
}
```

### 2. Get Product Information
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "Tell me about product '123'."
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "Product '123' is a high-quality widget."
}
```

### 3. List All Products
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "List all available products."
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "Available products: 123, 456, 789"
}
```

### 4. Get Warranty Policy
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "What is the warranty policy?"
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "All products come with a one-year warranty covering manufacturing defects."
}
```

### 5. Memory
#### Step 1: Ask for your name
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "Do you know my name?"
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "I don't know your name yet. Could you please tell me?"
}
```

#### Step 2: Tell your name
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "My name is Ivan."
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "Nice to meet you, Ivan!"
}
```

#### Step 3: Ask again
Request:
```http
POST /chat
Content-Type: application/json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "user_input": "Do you know my name now?"
}
```
Response:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
  "ai_response": "Yes, your name is Ivan."
}
```