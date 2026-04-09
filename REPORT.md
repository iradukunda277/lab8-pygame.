# Project Report: AI-Assisted Development

## 1. Initial Approach
* **Understanding:** The goal of Lab 8 was to build a PyGame moving-squares app while keeping control of the code and understanding the main loop, rendering, movement, and rotation. I started from a simple moving-squares version and then extended it step by step.
* **Assumptions:** I assumed the core deliverable was not just "something visual", but a project that I could explain clearly: setup, game loop, square data structure, movement, rotation, and later feature additions such as size-based speed and jitter.

## 2. Prompting & AI Interaction
* **Successes:** The best prompts were concrete and constrained. Asking for one feature at a time, asking for comments, and asking for explanations of specific functions helped me keep control. Requests like "add comments", "explain the rotation", and "implement only the missing feature" worked better than broad prompts.
* **Failures:** Broader AI-generated solutions tended to move too fast, especially when they introduced too much code at once. That made it harder to follow every design decision immediately. Another risk was adding features before checking whether they actually matched the PDF instructions.
* **Analysis:** These failures happened when the scope was too open or when I relied on the AI before fully checking the assignment materials. Narrower prompts, reading the PDFs carefully, and verifying each step against the assignment made the process more manageable.

## 3. Key Learnings
* **Technical Skills:** I improved my understanding of the PyGame event loop, frame updates, drawing rotated shapes, bounce logic, velocity vectors, and the idea of applying jitter by rotating a direction vector slightly over time. I also learned how to connect speed constraints to square size.
* **AI Workflow:** In future projects I would keep using AI in smaller steps, ask for more explanation and fewer big refactors, and check assignment requirements earlier. The biggest lesson is that AI is most useful when it supports my understanding instead of replacing it.
