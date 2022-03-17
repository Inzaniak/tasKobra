import subprocess
import sys
import pkgutil

PYTHON_PATH = sys.executable


def run(cmd):
    return subprocess.run(["powershell", "-Command", cmd], capture_output=True, shell=True)


class Task:

    def __init__(self, name, folder='', **kwargs):
        """A tasKobra Task object.

        Args:
            name (str): The name of the task.
            folder (str, optional): The folder to create the task in. Defaults to ''.
            debug (bool, optional): If True, will print the command being run. Defaults to False.
        """        
        self.name = name
        self.folder = folder
        self.existing = False
        self.python_path = PYTHON_PATH
        self.schedule_string = ''
        self.additional_args = {}
        self.check_task()
        self.debug = False
        self.__dict__.update(kwargs)
        self.last_run = {}
        
    
    def print(self, text):
        """Prints text to the console, if debug is True.

        Args:
            text (str): The text to print.
        """        
        if self.debug:
            print(text)
    
            
    def check_task(self):
        """Checks if the task exists.
        """    
        if self.folder == '':
            check_exists = run(f'Get-ScheduledTaskInfo -TaskName "{self.name}"')
        else:
            check_exists = run(f'Get-ScheduledTaskInfo -TaskName "{self.name}" -TaskPath "\\{self.folder}"')
        print(check_exists)
        if check_exists.returncode == 0:
            self.attrs = {el.split(':', 1)[0]: el.split(':', 1)[
                1] for el in check_exists.stdout.decode('utf-8').split('\r\n') if el != ''}
            self.attrs = {k.strip(): v.strip() for k, v in self.attrs.items()}
            self.folder = self.attrs['TaskPath']
            self.existing = True
            

    def set_schedule(self, schedule_string):
        """Set the schedule for the task.

        Args:
            schedule_string (str): A string representing the schedule.
        Examples: 
            -Daily -At 12:00:00
            -Once -At 03:00:00
        Check New-ScheduledTaskTrigger docs to learn more.
        """    
        self.schedule_string = schedule_string
        

    def create_task(self, script_full_path, user, password=None):
        """Creates a task in the windows task scheduler.

        Args:
            script_full_path (str): The full path to the script you want to run.
            user (str): The user to run the script as.
        """        
        if password:
            self.additional_args['-Password'] = password
        if self.schedule_string == '':
            self.print('No schedule set')
        elif self.existing:
            self.print(f'Task already exists: {self.folder}{self.name}')
        else:
            script_full_path = script_full_path.replace('\\', '/')
            script_name = script_full_path.split('/')[-1]
            script_path = '/'.join(script_full_path.split('/')[:-1])
            self.print(f'Creating task: {self.folder}{self.name}')
            run_script = pkgutil.get_data(__name__, "data/pipeline_template.ps1").decode('utf-8')
            run_script = run_script.format(python_path=self.python_path
                                        , task_name=self.name
                                        , task_folder=self.folder
                                        , script_path=script_path
                                        , script_name=script_name
                                        , task_user=user
                                        , repeat_schedule=self.schedule_string
                                        , additional_args = ' '.join(f'{k} {v}' for k, v in self.additional_args.items())
                                        )
            # print(run_script)
            subprocess.run(["powershell", "-Command", run_script])
            self.print(f'Task created: {self.folder}{self.name}')
            self.check_task()
            

    def delete_task(self):
        """Deletes a task from the windows task scheduler.
        """        
        if self.existing:
            self.print(f'Deleting task: {self.folder}{self.name}')
            if self.folder == '':
                run(f'Unregister-ScheduledTask -TaskName "{self.name}" -Confirm:$false')
            else:
                run(f'Unregister-ScheduledTask -TaskPath "\\{self.folder}" -TaskName "{self.name}" -Confirm:$false')
            self.print(f'Task deleted: {self.folder}{self.name}')
            self.existing = False
        else:
            self.print(f'Task does not exist: {self.folder}{self.name}')
            
            
    def disable_task(self):
        """Disables the task from the windows task scheduler.
        """        
        if self.existing:
            self.print(f'Disabling task: {self.folder}{self.name}')
            if self.folder == '':
                run(f'Disable-ScheduledTask -TaskName "{self.name}"')
            run(f'Disable-ScheduledTask -TaskName "{self.name}" -TaskPath "{self.folder}"')
            self.print(f'Task disabled: {self.folder}{self.name}')


    def enable_task(self):
        """Enables the task from the windows task scheduler.
        """        
        if self.existing:
            self.print(f'Enabling task: {self.folder}{self.name}')
            if self.folder == '':
                run(f'Enable-ScheduledTask -TaskName "{self.name}"')
            run(f'Enable-ScheduledTask -TaskName "{self.name}" -TaskPath "{self.folder}"')
            self.print(f'Task enabled: {self.folder}{self.name}')
           
            
    def run_task(self):
        """Runs the task from the windows task scheduler.
        """        
        if self.existing:
            self.print(f'Running task: {self.folder}{self.name}')
            if self.folder == '':
                run(f'Start-ScheduledTask -TaskName "{self.name}"')
            run(f'Start-ScheduledTask -TaskName "{self.name}" -TaskPath "{self.folder}"')
            self.print(f'Task run: {self.folder}{self.name}')
    
    
    def stop_task(self):
        """Stops the task from the windows task scheduler.
        """        
        if self.existing:
            self.print(f'Stopping task: {self.folder}{self.name}')
            if self.folder == '':
                run(f'Stop-ScheduledTask -TaskName "{self.name}"')
            run(f'Stop-ScheduledTask -TaskName "{self.name}" -TaskPath "{self.folder}"')
            self.print(f'Task stopped: {self.folder}{self.name}')
            
            
    def get_last_run(self):
        """Gets the last time the task was run.
        """        
        if self.existing:
            self.print(f'Getting last run time for task: {self.folder}{self.name}')
            if self.folder == '':
                results = run(f'Get-ScheduledTaskInfo -TaskName "{self.name}"').stdout.decode('utf-8')
            else:
                results = run(f'Get-ScheduledTaskInfo -TaskName "{self.name}" -TaskPath "{self.folder}"').stdout.decode('utf-8')
            self.last_run = {el.split(':', 1)[0]: el.split(':', 1)[
                1] for el in results.split('\r\n') if el != ''}
            self.last_run = {k.strip(): v.strip() for k, v in self.attrs.items()}
            self.print(f'Last run time for task: {self.folder}{self.name}')