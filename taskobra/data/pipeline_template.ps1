$Action = New-ScheduledTaskAction -Execute '{python_path}' -Argument '{script_name}' -WorkingDirectory '{script_path}'
$Trigger = New-ScheduledTaskTrigger {repeat_schedule}
$Settings = New-ScheduledTaskSettingsSet
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
Register-ScheduledTask -TaskName '{task_folder}{task_name}' -InputObject $Task -User '{task_user}' {additional_args}