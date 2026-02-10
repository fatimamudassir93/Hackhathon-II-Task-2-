# ReminderAgent

## Name
ReminderAgent

## Description
Sends notifications and reminders for tasks in the Todo application. This agent manages scheduling and delivery of alerts to help users stay on track with their tasks.

## Purpose
To provide timely notifications and reminders for upcoming tasks, deadlines, and important events, helping users maintain productivity and meet their commitments.

## Trigger Commands
- `/reminder schedule` - Schedule a reminder for a task
- `/reminder cancel` - Cancel an existing reminder
- `/reminder list` - List upcoming reminders
- `/reminder snooze` - Temporarily postpone a reminder

## Input
```json
{
  "action": "schedule|cancel|list|snooze",
  "taskId": "string (required for schedule/cancel/snooze)",
  "reminderTime": "string (ISO 8601 format, required for schedule)",
  "notificationMethod": "email|push|sms (optional, defaults to user preference)",
  "snoozeDuration": "number (minutes, required for snooze)",
  "userId": "string (required for list)"
}
```

## Output
```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "reminderId": "string",
    "taskId": "string",
    "reminderTime": "string (ISO 8601)",
    "notificationMethod": "email|push|sms",
    "status": "scheduled|sent|cancelled|snoozed",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  }
}
```

## Behavior Notes
- Validates reminder time to ensure it's in the future
- Supports multiple notification methods based on user preferences
- Handles timezone conversions for accurate reminder delivery
- Implements snooze functionality with configurable durations
- Maintains reminder status and updates accordingly
- Prevents duplicate reminders for the same task at the same time

## Example JSON Request
```json
{
  "action": "schedule",
  "taskId": "task_abc123",
  "reminderTime": "2026-01-10T09:00:00Z",
  "notificationMethod": "push"
}
```

## Confirmation Message
"Reminder scheduled successfully for task 'task_abc123' at 2026-01-10 09:00 AM UTC. You will receive a push notification at the scheduled time. You can cancel or modify this reminder using the reminder management commands."