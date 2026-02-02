# Menagerist Backend Architecture

This document describes the architectural approach used for the Menagerist backend.

The goal is to build a system that is straightforward to understand, testable, and readily adaptable to future shifts.

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

This combination keeps the core logic independent of technical details.

To keep the codebase more “Pythonic”, we use friendlier names for the hexagonal concepts:

- **Ports** → **Interfaces / Protocols** (contracts that inner layers depend on)
- **Adapters** → **Persistence / Integrations** (concrete implementations)

---

## Layers and Dependency Direction

Entrypoints
↓
Infrastructure (Persistence / Integrations)
↓
Application (Use Cases)
↓
Domain

Rules:

- Domain depends on nothing else
- Application depends only on Domain (and shared abstractions)
- Infrastructure depends on Application and Domain
- Entrypoints depend on everything inwards

Inner layers must never import outer layers.

---

## Domain Layer

The domain layer represents the business concepts.

It contains:
- Entities (Item, Event, Person, Location)
- Domain rules and invariants
- Value Objects

It does not contain:
- Databases
- Web frameworks
- Logging
- Configuration

The domain describes what the system is, not how it runs.

---

## Interfaces (Ports)

Interfaces are abstractions used by the application layer.

They describe:
- What capabilities the application needs (e.g. repository operations, unit of work, event publishing)
- What operations are required

They do not describe:
- How data is stored
- Which database is used
- Which external service is called

This allows:
- In-memory implementations for tests
- SQLAlchemy implementations for production
- Other implementations in the future

**Naming convention (recommended):**
- `XRepository`, `UnitOfWork`, `EventBus`, `Clock`, etc. for interfaces
- `SqlAlchemyXRepository`, `SqlAlchemyUnitOfWork`, etc. for implementations

---

## Application Layer (Use Cases)

The application layer contains **use-case logic**.

It contains:
- **Use cases** (one module/file per use case is preferred)
- Coordination/orchestration logic
- Transaction boundaries (via Unit of Work)
- Calls to interfaces (repositories, event bus, etc.)

It does not contain:
- HTTP request handling
- Database sessions
- Framework-specific code

The application layer answers:

What happens when a user does this?

---

## Use Cases (instead of Services)

Use cases replace the “service” concept.

A use case should be:
- Small and explicit (easy to test)
- Dependency-injected (takes interfaces/protocols)
- The place where transactions are coordinated (via UoW)
- Focused on one user intent (command/query)

Examples:
- Create an item
- Update an item
- List items
- Attach an event to an item

Use cases are reusable across:
- APIs
- CLIs
- Background jobs

---

## Overlapping Use Cases Between Features (Workflows)

Sometimes a business capability spans multiple features (e.g. onboarding, provisioning, multistep processes).

Instead of sharing “use cases” across features (which tend to tangle dependencies), create an explicit **workflow** module:

- Think: cross-feature orchestration that coordinates multiple use cases and interfaces.
- Workflows are still application-layer code, just scoped to a cross-cutting business process.

Recommended names/locations:
- `workflows/` (preferred)
- `processes/` (also fine)

Rule of thumb:
- Share *mechanisms* (utilities, interfaces), not *policies* (business decisions).
- If it’s a real business action spanning features, it deserves a workflow.

---

## Infrastructure (Persistence / Integrations)

Infrastructure provides concrete implementations.

It contains:
- **Persistence**: database implementations (e.g. SQLAlchemy repositories, mappings)
- **Integrations**: external APIs, message buses, email providers, etc.
- Dependency wiring / composition root

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
- Calling application use cases
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
- In-memory implementations are used for unit tests
- Architecture tests enforce dependency direction
- Integration tests are optional and limited in scope

Tests should be fast, deterministic, and easy to run.

---

## Guiding Principles

- Dependencies always point inward
- Frameworks are details
- Prefer clarity to cleverness
- Design for change
- Make the right thing easy

---

This architecture is intentionally boring.

Boring systems last longer.
