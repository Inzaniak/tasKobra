![tasKobra](images/logo.png)  
![tasKobra](images/banner.png)  
Taskobra is a lightweight and easy way to manage windows schedules programmatically.
It uses Powershell commands under the hood to create and delete tasks in the scheduler:  
```python
from taskobra import Task

task = Task('TaskName', 'TaskFolder\\')
task.set_schedule('-Daily -At 13:00:00')
task.delete_task() # DELETES THE TASK ONLY IF EXISTS
task.create_task('PATH/TO/SCRIPT.py', 'USERNAME') # WITH LOGGED IN USER 
task.create_task('PATH/TO/SCRIPT.py', 'USERNAME', 'PASSWORD')  # WITH OTHER USER
# ADDED IN v0.0.2 ###############
# Enable disable a task
task.disable_task()
task.enable_task()
# Start/Stop a Tast
task.run_task()
task.stop_task()
# Last Run Info
task.get_last_run()
print(task.last_run)
```
This package is a WIP and it's not meant to be used in production environments. **Use it at your own risk!**


---

## Installation
```
pip install git+https://github.com/Inzaniak/tasKobra@master
```
---
## Supported Features (v0.0.2)
- Task Creation
- Task Deletion
- Task Replacement
- Schedule Edit
- Task Enabling/Disabling
- Task Running/Stopping
- Get last task execution
---
## Made by
<img src="images/inzaniak.png" width="100" height="100">   

Personal Website: https://inzaniak.github.io