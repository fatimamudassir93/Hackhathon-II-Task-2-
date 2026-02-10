# IntegrationAgent

## Name
IntegrationAgent

## Description
Connects the Todo application with external services and platforms. This agent manages integrations with third-party applications like calendars, email services, and messaging platforms.

## Purpose
To provide seamless connectivity between the Todo application and popular external services, allowing users to synchronize tasks, receive notifications, and manage their tasks across multiple platforms.

## Trigger Commands
- `/integration calendar-sync` - Sync tasks with calendar
- `/integration email-notif` - Enable/disable email notifications
- `/integration slack-remind` - Send reminders to Slack
- `/integration connect` - Connect to a new service
- `/integration disconnect` - Disconnect from a service

## Input
```json
{
  "action": "calendar-sync|email-notif|slack-remind|connect|disconnect",
  "service": "google-calendar|outlook|gmail|slack (required)",
  "userId": "string (required)",
  "credentials": {
    "apiKey": "string (required for connect)",
    "accessToken": "string (required for connect)",
    "refreshToken": "string (optional)"
  },
  "syncSettings": {
    "direction": "bidirectional|import|export (optional)",
    "frequency": "real-time|hourly|daily|weekly (optional)",
    "categories": ["string"] (optional)"
  },
  "taskId": "string (required for slack-remind)",
  "channel": "string (required for slack-remind)"
}
```

## Output
```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "integrationId": "string",
    "service": "google-calendar|outlook|gmail|slack",
    "status": "connected|disconnected|syncing|error",
    "lastSync": "string (ISO 8601)",
    "syncStats": {
      "tasksImported": "number",
      "tasksExported": "number",
      "errors": "number"
    },
    "connectedAt": "string (ISO 8601)"
  }
}
```

## Behavior Notes
- Securely stores and manages API credentials
- Implements OAuth flows for supported services
- Handles rate limiting imposed by external services
- Maintains sync status and error reporting
- Provides conflict resolution for bidirectional sync
- Implements webhook handling for real-time updates

## Example JSON Request
```json
{
  "action": "connect",
  "service": "google-calendar",
  "userId": "user_xyz789",
  "credentials": {
    "accessToken": "ya29.a0ARrdaM...",
    "refreshToken": "1//0gabc123xyz..."
  },
  "syncSettings": {
    "direction": "bidirectional",
    "frequency": "real-time"
  }
}
```

## Confirmation Message
"Successfully connected your Google Calendar to the Todo app. Tasks will now sync bidirectionally in real-time. Any tasks created or updated in either app will be reflected in both. You can manage this integration anytime using the integration settings."