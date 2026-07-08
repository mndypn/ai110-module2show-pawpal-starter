# PawPal+ Project Reflection

## 1. System Design

- add pet/owner info, add/edit tasks, generate and display daily schedule

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The classes I used are:
Owner: attributes = name, pets / methods = add pet, view tasks
Pet: attributes = name, age, species, tasks / methods = add task
Task: attributes = description, due date, completion status, priority, duration / methods = mark complete, edit task
Scheduler: methods = filter tasks, sort tasks

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, Claude recommended to change the priority to a dictionary instead of a string because if it stays a string, the sorting method will sort it alphabetically instead of ranked by urgency. I made this change because this makes sense if I want the sorting to work as intended.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
