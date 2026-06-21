# Agent Styles and Methodologies

This document defines the set of `X = 5` programming styles for the experiment.

1. Stepwise Refinement
   - Start with the simplest correct implementation.
   - On each iteration, apply exactly ONE focused refinement (algorithm, idiom, or restructure).
   - Walk the run budget as a sequence of refinement steps; best.py preserves your best so far.

2. Functional Programming
   - Solve problems using pure functions, immutability, and composition.
   - Avoid side effects.
   - Prefer recursion, higher-order functions, and declarative style.

3. Object-Oriented Design
   - Use classes, encapsulation, and clear interfaces.
   - Model the problem domain with objects and responsibilities.
   - Favor extendability and structure.

4. Smart Pattern-Focused
   - Seek the most effective pattern, algorithm, or clever design.
   - Accept reduced readability in exchange for challenge-style sophistication.
   - Keep correctness as the top priority while leveraging advanced techniques.

5. Prototype-Driven / Proto
   - Assemble existing snippets and idioms quickly.
   - Iterate on a working prototype until it passes validation.
   - Prioritize rapid progress over initial elegance.
   - Refine incrementally after getting correctness.

## How to use these styles

- Each agent folder should declare its style and a short prompt guideline.
- During execution, the agent should follow the assigned methodology.
- The same task must be solved by all agents, but with different implementation patterns.
