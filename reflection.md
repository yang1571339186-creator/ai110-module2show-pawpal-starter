# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

### My initial diagram had the following classes:
* Owner: This will be the user class, this initially only had a owner name and schedule saved as a string
* The owner then has many pet class, which has field referencing the owner, and fields  containing information about its name and species. 
* The owner also has a schedule class, which has the class scheduler built into it to handle to log of creating a schedule. 
* Then the task class which has information about its priority which pets it's for. The schedule class uses the task class to determine scheudle itself which will be a list of string.



**b. Design changes**

### Design Changes
I made several design changes, the biggest of which is the timeslot class which is by the owner class. The timeslot classes takes an users available start and end time and parses it into the class. The timeslot classs made it much clean and easier to design the algorithmic features of the scheduler as well as made it easier to parse the user time strings to a python-usable field

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- Constraints that it uses is the priority of the tasks, the time it takes for a task to complete, as well as user preference for morning or nights
- My decision was that the available time is the most important constraint to consider. This is because we would want to respect the owners time and only enter tasks that they can finish. Additionally, owners have the ability to edit tasks and it duration so that it can fit into a timeslot

**b. Tradeoffs**

- One tradeoff I made was that, in the case where there is multiple tasks of the same priority. I decided to first add the task that takes the least amount of time. This way, we can implement a sort of greedy algorithm where we maximum the amount of tasks we can fit in a timeslot in respect to the available time and task priorities

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to format the diagrams using my vision for the design. Additionally, the AI was helpful in creating tests and helping with the UI elements.
- I find that the AI responds to the best prompts where the prompts are specific and well designed. For example, I already had the algothrimic idea in mind for how we would validate that a timeslot is valid(hh:mm format, no overlaps) and prompting the AI to write with these constraints in mind was more product than a more vague prompt.

**b. Judgment and verification**

- While implementing the check-box button, the AI had initially suggested an implementation where the schedule is regenerated every time the user checks off a the box. I rejected this suggestion based on the expected user behavior where the users are expected to work off the schedule and should only need to regenerate if they are done for the day or if they've made changes to the tasks/pets. Thus, I made the decision to not automatically regerenate the schedule but give user a button to do so. 

---

## 4. Testing and Verification

**a. What you tested**

My test suite in `tests/test_pawpal.py` were mainly focused on the important aspects of scheduling

- I had implements tests for the parsing method for the timeslot class to ensure that parsing for start_time/end_time string into appropriate timeslot objects

- Then the rest of test were focused on the algorithms in the scheduler object class. This included tasks of various priorities in the sorting alogrithm. Tasks of various start times for the filter algorithm as well as the create schduele algorithm to ensure that the scheulder works well with the tasks and owner preferences. 

**b. Confidence**

- I trust that the scheduler works as intended but there is some additional features I would've liked to add to the scheduler
- Some edge cases include been timeslots where the start time is after the end time and check for that potential error.

---

## 5. Reflection

**a. What went well**

- overall I'm pretty happy with the design and I like the use of the Timeslot class to simplify the algorithma and scheduler features.  

**b. What you would improve**

- I would wanted to add a feature where you can dedicate a timeslot to a task and build around. Such you can add that they have available time from 7-9 but already have an vet appointment from 8 - 8:30. 

**c. Key takeaway**

- I learned that AI can work best when you already have an idea as well as help explor ideas to build your system; but not necessarily both at the same plan. That is, you can use AI to help to explore ideas and plans as well as creating skeleton to implement them; but asking AI to implement code with a vague plan can to problematic. 
