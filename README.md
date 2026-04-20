# Agent Discovery + Usage Platform

A simplified FastAPI system to register agents, search through them, and track their interactions with strictly enforced idempotency.

## Setup and Running

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the Server**:
   ```bash
   python main.py
   ```
   The server will start at `http://localhost:8000`. You can access the interactive Swagger UI at `http://localhost:8000/docs`.

## Technical Features
- **Agent Registry**: Register agents with name, description, and endpoint.
- **Search**: Case-insensitive substring matching on name and description.
- **Idempotent Usage Logging**: Uses `request_id` to ensure that duplicate usage reports (e.g., from network retries) do not result in double counting.
- **Keyword Extraction**: Automatically generates tags from the agent description by filtering common stop words.

---

## Design Questions (REQ 5)

### 1. How would you extend this system to support billing without double charging?
To support reliable billing, I would implement a "Write-Ahead Ledger" pattern. Every usage event would be stored in a persistent database with a unique constraint on the `request_id`. Before deducting credits, the system would check the ledger to see if that specific `request_id` has already been billed. Using atomic database transactions ensures that the balance update and the ledger entry happen together (all or nothing), preventing double charging even in high-concurrency environments.

### 2. How would you store this data if scale increases (100K agents)?
For 100K agents and high-volume usage logs, I would transition from in-memory storage to a persistent database like **PostgreSQL**. I would use **Full-Text Search (GIN indexes)** on the name and description fields to keep the `/search` endpoint fast. For the usage logs, which would grow rapidly, I would use a **Time-Series database extension (like TimescaleDB)** or a horizontal scaling solution like **Cassandra**. I would also implement a **Redis cache** to store the set of recently processed `request_id`s for near-instant idempotency checks before hitting the main database.

---

## Reflection on AI Usage - PART B
**a. Use of AI**: Yes, I used an AI assistant to help structure the FastAPI boilerplate and suggest the regex for keyword extraction.
**b. Modifications**: I manually implemented the `DataStore` class to encapsulate the state and refined the idempotency logic to ensure it specifically checked the `request_id` before any validation errors occurred. I also wrote the high-level design answers based on my understanding of distributed systems.
**c. Non-reliance on AI**: I did not rely on AI for the core business logic setup or the decision to use a Set for `request_id` tracking, as that requires a specific understanding of the problem's constraints.
