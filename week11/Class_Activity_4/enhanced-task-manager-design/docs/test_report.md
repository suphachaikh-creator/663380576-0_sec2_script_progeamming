# Week 11 Task Manager Test Report

CLI walkthrough used a temporary copy of `data/tasks.json`; the original data file was not modified.

## Results

- PASS — menu 1 adds normal task
- PASS — menu 2 adds due date task
- PASS — menu 3 adds priority task
- PASS — menu 4 lists tasks
- PASS — menu 5 completes task ID 2
- PASS — menu 6 deletes task ID 5
- PASS — menu 7 case-insensitive search
- PASS — menu 8 filters High priority
- PASS — menu 9 sorts by due date
- PASS — menu 0 exits

## Additional checks

- PASS — search matches descriptions and tags case-insensitively.
- PASS — priority and tag filters return the expected tasks.
- PASS — tasks with due dates sort before tasks without due dates.
- PASS — original `data/tasks.json` remained unchanged.

## Additional boundary checks

- PASS — combined status + priority + tag filters.
- PASS — priority ascending.
- PASS — priority descending.
- PASS — due date descending keeps undated tasks last.
- PASS — invalid due date rejected.
- PASS — invalid sort criterion rejected.
