![tasKobra](images/logo.png)  
Taskobra is a lightweight and easy way to manage windows schedules programmatically.
It uses Powershell commands under the hood to create and delete tasks in the scheduler:  
```python
from taskobra import Task

task = Task('TaskName', 'TaskFolder\\')
task.set_schedule('-Daily -At 13:00:00')
task.delete_task() # DELETES THE TASK ONLY IF EXISTS
task.create_task('PATH/TO/SCRIPT.py', 'USERNAME') # WITH LOGGED IN USER 
task.create_task('PATH/TO/SCRIPT.py', 'USERNAME', 'PASSWORD')  # WITH OTHER USER
```

---

## Installation
```
pip install git+https://github.com/Inzaniak/tasKobra@master
```
---
## Supported Features (v0.0.1)
- Task Creation
- Task Deletion
- Task Replacement
- Schedule Edit
---
## Made by
![My Logo](images/inzaniak.png)  
Personal Website: https://inzaniak.github.io