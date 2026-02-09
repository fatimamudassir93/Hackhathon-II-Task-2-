# AnalyticsAgent

## Name
AnalyticsAgent

## Description
Provides insights and analytics about task completion, productivity, and user behavior in the Todo application. This agent generates reports and statistics to help users understand their productivity patterns.

## Purpose
To analyze task data and generate meaningful insights about user productivity, task completion rates, and behavioral patterns to help users improve their task management effectiveness.

## Trigger Commands
- `/analytics count` - Get total task counts
- `/analytics completed` - Get completed tasks statistics
- `/analytics pending` - Get pending tasks statistics
- `/analytics report` - Generate productivity report
- `/analytics trends` - Get productivity trends over time

## Input
```json
{
  "action": "count|completed|pending|report|trends",
  "userId": "string (required)",
  "timeRange": "today|week|month|quarter|year|custom (optional, defaults to week)",
  "startDate": "string (ISO 8601, required for custom timeRange)",
  "endDate": "string (ISO 8601, required for custom timeRange)",
  "groupBy": "day|week|month (optional, for trends)",
  "includeTags": ["string"] (optional, for filtering)",
  "excludeTags": ["string"] (optional, for filtering)"
}
```

## Output
```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "summary": {
      "totalTasks": "number",
      "completedTasks": "number",
      "pendingTasks": "number",
      "completionRate": "number (percentage)",
      "averageCompletionTime": "number (hours)"
    },
    "trends": [
      {
        "date": "string (ISO 8601)",
        "completed": "number",
        "pending": "number"
      }
    ],
    "topTags": [
      {
        "tagName": "string",
        "taskCount": "number",
        "completionRate": "number (percentage)"
      }
    ],
    "productivityScore": "number (0-100)",
    "recommendations": ["string"]
  }
}
```

## Behavior Notes
- Calculates statistics based on user's task history
- Provides personalized recommendations based on productivity patterns
- Handles different time ranges for analysis
- Maintains privacy by only showing user-specific data
- Updates analytics in real-time as tasks are completed
- Generates actionable insights to improve productivity

## Example JSON Request
```json
{
  "action": "report",
  "userId": "user_xyz789",
  "timeRange": "month"
}
```

## Confirmation Message
"Productivity report generated for user 'user_xyz789' covering the past month. You completed 85% of your tasks with an average completion time of 2.3 days. Your most productive day was Tuesday with 4 completed tasks. Consider focusing on high-priority tasks during your peak productivity hours."