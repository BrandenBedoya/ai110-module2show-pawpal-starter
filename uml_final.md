# PawPal+ UML — Final (Phase 6)

> Render in VS Code with Mermaid Preview, or paste into https://mermaid.live
> Updated to reflect final implementation in pawpal_system.py

```mermaid
classDiagram
    class Task {
        +str description
        +str time
        +str frequency
        +str pet_name
        +str status
        +date due_date
    }

    class Pet {
        +str name
        +str species
        +int age
        +list~Task~ tasks
        +add_task(task: Task) None
        +get_tasks() list~Task~
    }

    class Owner {
        +str name
        +str email
        +list~Pet~ pets
        +add_pet(pet: Pet) None
        +get_all_tasks() list~Task~
    }

    class Scheduler {
        +Owner owner
        +__init__(owner: Owner)
        +get_all_tasks() list~Task~
        +sort_by_time() list~Task~
        +filter_tasks(status: str|None, pet_name: str|None) list~Task~
        +mark_complete(task: Task) None
        +detect_conflicts() list~str~
    }

    Owner "1" *-- "0..*" Pet : owns
    Pet "1" *-- "0..*" Task : owns
    Scheduler --> Owner : reads from
    Scheduler ..> Task : mutates
```

## Changes from Phase 1 draft

| Item | Draft | Final |
|---|---|---|
| `filter_tasks` signature | `(status, pet_name)` | `(status: str\|None, pet_name: str\|None)` — explicitly optional |
| `Owner → Pet` arrow | `-->` association | `*--` composition (Owner owns Pets, they don't exist independently) |
| `Pet → Task` arrow | `-->` association | `*--` composition (same reason) |
| `Scheduler → Task` | not shown | `..>` dashed — Scheduler mutates Tasks via `mark_complete()` |
```
