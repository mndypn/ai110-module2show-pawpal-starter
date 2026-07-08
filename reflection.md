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
Yes, Claude recommended to change the priority to a dictionary instead of a string because if it stays a string, the sorting method will sort it alphabetically instead of ranked by urgency. I made this change because this makes sense if I want the sorting to work as intended. It also added a build schedule method in order to generate the schedule.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler looks at 4 things: available time, priority (high/medium/low), due
date/time, and duration. It also skips tasks that are already done. Due date and
priority mattered most because the owner needs urgent care like meds or walks to
happen first. Available time is the hard limit everything has to fit into.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler uses a greedy method: it sorts tasks by urgency, then adds them one by one until the time runs out, skipping any that don't fit. This doesn't always fit the most tasks possible, but it's simple and easy to explain as the owner always sees their most important tasks first. For planning a pet's day, getting the important care done firstmatters more than squeezing in the most tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used different modes for the AI (plan, agent) to brainstorm ideas and then debug parts of the code and implement the app. Prompts that clarified the kind of edit/response needed were the most helpful.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
When I asked about potential logic bottlenecks and missing relationships, Claude kept suggesting to add unnecessary complexity and methods, so I had to determine which changes actually were needed.


**c. AI Strategy**

- **Which AI coding assistant features were most effective for building your scheduler?**

The most effective feature was being able to attach my actual files so the assistant's suggestions matched my real code instead of generic examples it referenced my exact method names.

- **Give one example of an AI suggestion you rejected or modified to keep your system design clean.**

When wiring conflict warnings into the Streamlit UI, one option was to change Scheduler.detect_conflicts() to return structured objects (dicts) so the UI could format them however it wanted. I kept the Scheduler returning simple human-readable warning strings and did the small display tweak in`app.py instead. This kept the Scheduler's job clean and unchanged as it stays a pure logic/service class while the UI stays responsible for presentation.

- **How did using separate chat sessions for different phases help you stay organized?**

Keeping design, implementation, and documentation in separate sessions meant each conversation stayed focused on one goal. This made it easier to find past decisions, avoided mixing unrelated context, and kept each phase's reasoning self-contained so I could revisit any one part without scrolling through everything else.

- **Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.**

I learned that even with a powerful AI helping, I still have to lead the design. The AI can generate lots of ideas fast, but I have to choose what fits the project, keep things simple, and make sure every suggestion matches the requirements. Being the architect means setting the direction, checking the AI’s work, and trimming anything unnecessary. The AI speeds things up, but I’m responsible for the final design.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested marking tasks complete, adding tasks to a pet, sorting by urgency and by time of day, daily recurrence creating the next task, conflict detection (flagging same-time tasks and not flagging different times/days), building a schedule within a time budget, skipping completed tasks, and editing with validation. These were important because they are the actual logic of the app. If sorting, conflicts, or the time budget are wrong, the whole schedule is wrong, so I
wanted to prove each one works.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident, since all 13 tests pass and they cover each main behavior,
including a few tricky cases (same day but different times should not conflict). With
more time I'd test edge cases like overlapping durations (an 08:00 30-minute task and
an 08:15 task), an empty task list, weekly recurrence across a month boundary, and a
time budget of 0.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with the scheduler logic. Sorting, conflict warnings, and the daily
schedule all work together, and having tests that pass makes me trust it.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I'd improve the conflict detection so it catches tasks whose times overlap, not just
tasks at the exact same time. I'd also add a way to reschedule or delete tasks in the
app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
My biggest takeaway is that a clear design makes everything easier. Planning the
classes first and keeping the logic separate from the UI made the code simpler to build
and test, and it helped me guide the AI instead of just accepting whatever it gave me.
