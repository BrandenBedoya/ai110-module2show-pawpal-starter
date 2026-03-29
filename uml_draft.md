# PawPal+ UML — Draft (Phase 1)

> Render this in VS Code with the Mermaid Preview extension, or paste into https://mermaid.live

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
        +filter_tasks(status, pet_name) list~Task~
        +mark_complete(task: Task) None
        +detect_conflicts() list~str~
    }

    Owner "1" --> "0..*" Pet : has
    Pet "1" --> "0..*" Task : has
    Scheduler --> Owner : manages
```

## Relationships

| Relationship | Type | Notes |
|---|---|---|
| Owner → Pet | One-to-many composition | An Owner holds a list of Pet objects |
| Pet → Task | One-to-many composition | A Pet holds a list of Task objects |
| Scheduler → Owner | Association | Scheduler reads from Owner; doesn't own it |
