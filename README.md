# Velora: Digital Wallet Microservices Architecture

## Overview

This project is a **production-ready, dockerized digital wallet system** built using a **microservices architecture**. It is designed with scalability, security, and separation of concerns in mind.

The system consists of the following core services:

* **AuthService** – Handles authentication, authorization, OTP, and JWT generation
* **WalletService** – Manages wallet balances, credits, debits, and wallet-related operations
* **OrchestratorService** – Coordinates distributed transactions (SAGA-based orchestration)
* **API Gateway** – Acts as a single entry point for all client requests

Each service is independently deployable and communicates over internal APIs.


---

## Services Breakdown

### 1. AuthService

**Responsibility:** User authentication and authorization

**Features:**

* User registration and login
* OTP generation and verification
* OAuth2-based authentication support
* JWT access token generation and validation

**Tech Stack:**

* Database: **PostgreSQL** (user data)
* Cache: **Redis** (OTP storage with TTL)
* Security: JWT, OAuth2

**Why Redis for OTP?**

* Fast read/write
* TTL-based automatic expiration
* Stateless OTP verification

---

### 2. WalletService

**Responsibility:** Wallet state and transaction handling

**Features:**

* Wallet creation per user
* Credit and debit operations
* Balance checks
* Wallet integrity enforcement

**Databases:**

* **PostgreSQL** – Wallet state (balance, wallet metadata)
* **MongoDB** – Transaction-related data

  * TransactionAuthLog
  * Transaction history
  * Audit and trace logs

**Why PostgreSQL + MongoDB?**

* PostgreSQL ensures **ACID consistency** for wallet balances
* MongoDB efficiently stores **high-volume, append-only transaction logs**

---

### 3. OrchestratorService

**Responsibility:** Distributed transaction coordination

**Key Role:**

* Implements **SAGA-based transaction orchestration**
* Ensures atomicity across services without using a shared database
* Handles:

  * Compensation logic
  * Rollbacks on failure
  * Transaction consistency

**Characteristics:**

* Stateless
* No database
* Acts as a coordinator, not a data owner

---

### 4. API Gateway

**Responsibility:** Unified entry point for clients

**Features:**

* Request routing to internal services
* Authentication middleware
* Rate limiting (optional)
* Centralized request validation

**Characteristics:**

* Stateless
* No database

---

## Data Flow Example (Wallet Payment)

1. Client sends payment request → API Gateway
2. API Gateway validates JWT via AuthService
3. Request forwarded to OrchestratorService
4. Orchestrator initiates SAGA transaction
5. WalletService:

   * Validates balance
   * Deducts amount
   * Logs transaction in MongoDB
6. Orchestrator confirms completion or triggers compensation on failure

---

## Technology Stack

* **Backend:** Microservices (REST APIs)
* **Authentication:** JWT, OAuth2, OTP
* **Databases:**

  * PostgreSQL
  * MongoDB
  * Redis
* **Containerization:** Docker, Docker Compose
* **Architecture Pattern:**

  * Microservices
  * API Gateway
  * SAGA (Orchestrated Transactions)

---

## Docker & Deployment

* Each service runs in its own Docker container
* Databases are containerized
* Environment-based configuration
* Ready for deployment on:

  * Docker Compose
  * Kubernetes (with minimal changes)

---

## Key Design Principles

* **Single Responsibility per Service**
* **No Shared Databases Across Services**
* **Stateless Services Where Possible**
* **Eventual Consistency via SAGA Pattern**
* **Security-First Authentication Design**

---

## Future Improvements

* Event-driven communication using Kafka/RabbitMQ
* Centralized logging and monitoring (ELK, Prometheus)
* Distributed tracing (OpenTelemetry)
* Circuit breakers and retries
* Fine-grained RBAC

---

## Conclusion

This project demonstrates a **real-world fintech-grade digital wallet backend**, emphasizing:

* Security
* Scalability
* Fault tolerance
* Clean microservice boundaries

It is suitable as a foundation for fintech applications, hackathons, or production systems.
