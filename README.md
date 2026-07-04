# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
![alt text](image.png)

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
tests/test_pawpal.py::TestTimeSlot::test_timeslot_creation PASSED                                                                                                                                  [  3%]
tests/test_pawpal.py::TestTimeSlot::test_timeslot_parse_valid PASSED                                                                                                                               [  6%]
tests/test_pawpal.py::TestTimeSlot::test_timeslot_parse_with_spaces PASSED                                                                                                                         [  9%]
tests/test_pawpal.py::TestTimeSlot::test_duration_minutes_one_hour PASSED                                                                                                                          [ 12%]
tests/test_pawpal.py::TestTimeSlot::test_duration_minutes_thirty_minutes PASSED                                                                                                                    [ 15%]
tests/test_pawpal.py::TestTimeSlot::test_duration_minutes_eight_hours PASSED                                                                                                                       [ 18%]
tests/test_pawpal.py::TestTimeSlot::test_duration_minutes_with_mixed_times PASSED                                                                                                                  [ 21%]
tests/test_pawpal.py::TestTimeSlot::test_conflicts_with_overlapping_start PASSED                                                                                                                   [ 24%]
tests/test_pawpal.py::TestTimeSlot::test_conflicts_with_overlapping_end PASSED                                                                                                                     [ 27%]
tests/test_pawpal.py::TestTimeSlot::test_conflicts_with_completely_overlapping PASSED                                                                                                              [ 30%]
tests/test_pawpal.py::TestTimeSlot::test_conflicts_with_no_overlap_before PASSED                                                                                                                   [ 33%]
tests/test_pawpal.py::TestTimeSlot::test_conflicts_with_no_overlap_after PASSED                                                                                                                    [ 36%]
tests/test_pawpal.py::TestTimeSlot::test_conflicts_with_adjacent_times PASSED                                                                                                                      [ 39%]
tests/test_pawpal.py::TestTimeSlot::test_timeslot_repr PASSED                                                                                                                                      [ 42%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_single_high PASSED                                                                                                                [ 45%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_mixed_order PASSED                                                                                                                [ 48%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_all_same PASSED                                                                                                                   [ 51%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_empty_list PASSED                                                                                                                 [ 54%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_multiple_high_and_low PASSED                                                                                                      [ 57%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_defaults_to_incomplete PASSED                                                                                                     [ 60%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_completed_only PASSED                                                                                                             [ 63%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_recurring_always_included PASSED                                                                                                  [ 66%]
tests/test_pawpal.py::TestScheduler::test_sort_tasks_by_priority_recurring_incomplete_in_completed_view PASSED                                                                                     [ 69%]
tests/test_pawpal.py::TestCreateDailySchedule::test_returns_dict_keyed_by_time_slots PASSED                                                                                                        [ 72%]
tests/test_pawpal.py::TestCreateDailySchedule::test_no_tasks_gives_empty_lists PASSED                                                                                                              [ 75%]
tests/test_pawpal.py::TestCreateDailySchedule::test_task_placed_into_available_slot PASSED                                                                                                         [ 78%]
tests/test_pawpal.py::TestCreateDailySchedule::test_all_fitting_tasks_scheduled PASSED                                                                                                             [ 81%]
tests/test_pawpal.py::TestCreateDailySchedule::test_higher_priority_scheduled_first PASSED                                                                                                         [ 84%]
tests/test_pawpal.py::TestCreateDailySchedule::test_task_too_long_not_scheduled PASSED                                                                                                             [ 87%]
tests/test_pawpal.py::TestCreateDailySchedule::test_slot_capacity_respected PASSED                                                                                                                 [ 90%]
tests/test_pawpal.py::TestCreateDailySchedule::test_morning_preference_fills_earliest_slot_first PASSED                                                                                            [ 93%]
tests/test_pawpal.py::TestCreateDailySchedule::test_night_preference_fills_latest_slot_first PASSED                                                                                                [ 96%]
tests/test_pawpal.py::TestCreateDailySchedule::test_no_preference_keeps_original_slot_order PASSED      
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_tasks_by_priority|In this method, task is sorted by priority with the lower index indicating higher priority |
| Filtering | filter_tasks_by_time| Given a time parameter, only display tasks that that have can be finished within that time. The method also calls sort_tasks_by_priority
by default so the higher priority tasks are shown first|
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
