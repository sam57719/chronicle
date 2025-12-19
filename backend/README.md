# Menagerist Backend Architecture

This document describes the architectural approach used for the Menagerist backend.

The goal is to build a system that is easy to understand, easy to test, and easy to change over time.

---

## Core Ideas

- Business logic is more important than frameworks
- Dependencies must always point inward
- Infrastructure is replaceable
- Testing should not require a database or web server
- The system should evolve without large rewrites

---

## Architectural Style

Menagerist uses:

- Domain-Driven Design (DDD)
- Hexagonal Architecture (Ports and Adapters)
- Fully typed, modern Python
- Async where appropriate

This combination keeps the core logic independent from technical details.

---

## Layers and Dependency Direction

Entrypoints  
↓  
Infrastructure  
↓  
Application  
↓  
Domain

Rules:

- Domain depends on nothing else
- Application depends only on Domain
- Infrastructure depends on Application and Domain
- Entrypoints depend on everything inward

Inner layers must never import outer layers.

---

## Domain Layer

The domain layer represents the business concepts.

It contains:
- Entities (Item, Event, Person, Location)
- Domain rules and invariants
- Repository interfaces (ABCs or Protocols)

It does not contain:
- Databases
- Web frameworks
- Logging
- Configuration

The domain describes what the system is, not how it runs.

---

## Repository Interfaces

Repositories are abstractions defined in the domain layer.

They describe:
- What data the application needs
- What operations are required

They do not describe:
- How data is stored
- Which database is used

This allows:
- In-memory repositories for tests
- SQLAlchemy repositories for production
- Other storage mechanisms in the future

---

## Application Layer

The application layer contains use-case logic.

It contains:
- Services (for example: ItemService)
- Coordination logic
- Unit of Work interfaces

It does not contain:
- HTTP request handling
- Database sessions
- Framework-specific code

The application layer answers:

What happens when a user does this?

---

## Services

Services group related operations for a domain concept.

Examples:
- Creating an item
- Updating an item
- Listing items
- Attaching events to items

Services are reusable across:
- APIs
- CLIs
- Background jobs

---

## Infrastructure Layer

The infrastructure layer provides concrete implementations.

It contains:
- SQLAlchemy repositories
- Database configuration
- Logging setup
- Dependency container / wiring

Infrastructure implements interfaces defined by inner layers.

Infrastructure is allowed to change without affecting the domain or application logic.

---

## Entrypoints

Entrypoints are how the outside world interacts with the application.

Examples:
- FastAPI
- CLI commands

Entrypoints are responsible for:
- Parsing input
- Validating request shape
- Calling application services
- Formatting output

Entrypoints do not contain business logic.

---

## Configuration

- Runtime configuration uses Pydantic settings
- Application metadata is read from pyproject.toml
- Configuration is injectable and override-friendly
- Settings are not hard-coded into the application logic

---

## Validation

Validation happens at multiple levels:

- Entrypoints validate input shape and types
- Application layer validates workflows and cross-entity rules
- Domain enforces invariants that must always hold

The database is not relied upon for correctness.

---

## Testing Philosophy

- Domain and application logic are tested without infrastructure
- In-memory repositories are used for unit tests
- Architecture tests enforce dependency direction
- Integration tests are optional and limited in scope

Tests should be fast, deterministic, and easy to run.

---

## Guiding Principles

- Dependencies always point inward
- Frameworks are details
- Prefer clarity over cleverness
- Design for change
- Make the right thing easy

---

This architecture is intentionally boring.

Boring systems last longer.
