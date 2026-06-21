# LRU Cache

## Language
Python

## Goal
Implement a class **`LRUCache`** with `__init__(self, capacity)`, `get(key)`, and `put(key, value)` — a fixed-capacity LRU (least-recently-used) cache. The class name must be exactly `LRUCache` (the grader instantiates `LRUCache(capacity)`).

## Rules
- A positive integer `capacity` needs to be set dynamically as input that never changes and reflects storage capacity.
- `get(key)` returns the stored value if present, otherwise `-1`. A successful `get` counts as a use and refreshes the key's recency.
- `put(key, value)` inserts a new key or updates an existing one; either way it refreshes the key's recency.
- When inserting a **new** key would exceed `capacity`, evict the least-recently-used key first.

## Example
Capacity = 2, then:
1. `put(1, 1)`
2. `put(2, 2)`
3. `get(1)` → `1`
4. `put(3, 3)` → evicts key `2` (least recently used)
5. `get(2)` → `-1`

## Verification
Graded against a hidden test suite; you receive only a verdict (`correct`, `passed`/`total`) and metrics - never the test inputs or expected outputs. It exercises: eviction order under interleaved `get`/`put`, recency refresh on both reads and updates, capacity-1 caches, and repeated keys.
