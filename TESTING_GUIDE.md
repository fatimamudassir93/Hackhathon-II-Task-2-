# Full Stack Testing Guide - TODO App with AI Chatbot

## Overview

This guide walks you through testing the complete TODO application with the newly organized chatbot functionality.

---

## Prerequisites

- Node.js 18+ installed
- Python 3.10+ installed
- PostgreSQL database (Neon DB configured)
- LLM API key (OpenAI, Groq, or Gemini)

---

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Configure environment variables
# Edit backend/.env and add:
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies (if not already done)
npm install

# Verify .env configuration
# Should have:
# BACKEND_URL=http://localhost:8000
# BETTER_AUTH_SECRET=...
# DATABASE_URL=...
```

---

## Running the Application

### Terminal 1: Start Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify Backend:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","service":"Todo App API"}
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 14.2.35
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

---

## Testing Checklist

### ✅ 1. Backend Health Check

**Test:**
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status":"healthy","service":"Todo App API"}
```

### ✅ 2. API Documentation

**Test:**
Open in browser: http://localhost:8000/docs

**Expected:**
- Swagger UI loads
- See all endpoints (auth, tasks, chat)
- Can test endpoints interactively

### ✅ 3. Frontend Access

**Test:**
Open in browser: http://localhost:3000

**Expected:**
- Landing page loads
- See sign in/sign up options
- No console errors

### ✅ 4. User Registration

**Test:**
1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter email, password, name
4. Submit

**Expected:**
- Registration succeeds
- Redirected to dashboard
- User session created

### ✅ 5. User Sign In

**Test:**
1. Go to http://localhost:3000/sign-in
2. Enter credentials
3. Submit

**Expected:**
- Sign in succeeds
- Redirected to dashboard
- Session persists

### ✅ 6. Dashboard Access

**Test:**
Navigate to http://localhost:3000/dashboard

**Expected:**
- Dashboard loads
- Shows task list (empty or with tasks)
- Navigation bar visible

### ✅ 7. Chat Interface Access

**Test:**
Navigate to http://localhost:3000/chat

**Expected:**
- Chat interface loads
- Shows welcome message
- Input field ready
- No errors in console

### ✅ 8. Send Chat Message

**Test:**
1. Go to http://localhost:3000/chat
2. Type: "Add a task to buy groceries"
3. Press Enter or click Send

**Expected:**
- Message appears in chat
- Loading indicator shows
- AI response appears
- Tool call displayed (add_task)
- No errors

### ✅ 9. Task Management via Chat

**Test Commands:**

**Add Task:**
```
Add a task to buy groceries
```
Expected: Task created, confirmation message

**List Tasks:**
```
List all my tasks
```
Expected: Shows all tasks with IDs

**Complete Task:**
```
Complete task [task_id]
```
Expected: Task marked complete

**Delete Task:**
```
Delete task [task_id]
```
Expected: Task deleted

### ✅ 10. Tag Management via Chat

**Test Commands:**

**Add Tag:**
```
Add tag urgent to task [task_id]
```
Expected: Tag added

**List Tags:**
```
Show all my tags
```
Expected: Lists all unique tags

**Filter by Tag:**
```
Show tasks with tag urgent
```
Expected: Shows filtered tasks

### ✅ 11. Reminder Management via Chat

**Test Commands:**

**Schedule Reminder:**
```
Remind me about task [task_id] tomorrow at 10am
```
Expected: Reminder scheduled

**List Reminders:**
```
List all my reminders
```
Expected: Shows all reminders

### ✅ 12. Analytics via Chat

**Test Commands:**

**Count Tasks:**
```
How many tasks do I have?
```
Expected: Returns total count

**Completed Tasks:**
```
How many tasks are completed?
```
Expected: Returns completed count

**Pending Tasks:**
```
How many tasks are pending?
```
Expected: Returns pending count

### ✅ 13. Chat History

**Test:**
1. Send several messages
2. Refresh the page
3. Check if history loads

**Expected:**
- Previous messages appear
- Conversation preserved
- Timestamps shown

### ✅ 14. Error Handling

**Test:**
1. Stop backend server
2. Try sending a chat message

**Expected:**
- Error message displayed
- User informed of connection issue
- No crash

### ✅ 15. Tool Call Display

**Test:**
Send a message that triggers tools (e.g., "Add a task")

**Expected:**
- Tool name displayed
- Tool status shown (created/updated/etc.)
- Visual indicator (gear icon)

---

## Common Issues & Solutions

### Issue: "Failed to send message"

**Symptoms:**
- Error appears in chat
- Message not sent

**Solutions:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check LLM API key is configured in backend/.env
3. Check browser console for detailed error
4. Verify BACKEND_URL in frontend/.env

### Issue: "Unauthorized" Error

**Symptoms:**
- 401 error in console
- Redirected to sign in

**Solutions:**
1. Sign out and sign in again
2. Clear browser cookies
3. Check BETTER_AUTH_SECRET matches in both .env files

### Issue: Backend Won't Start

**Symptoms:**
- Import errors
- Module not found

**Solutions:**
1. Verify Python version: `python --version` (should be 3.10+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check virtual environment is activated
4. Verify all chatbot files are in place

### Issue: Frontend Won't Start

**Symptoms:**
- npm errors
- Module not found

**Solutions:**
1. Delete node_modules: `rm -rf node_modules`
2. Delete package-lock.json: `rm package-lock.json`
3. Reinstall: `npm install`
4. Check Node version: `node --version` (should be 18+)

### Issue: Chat Not Responding

**Symptoms:**
- Loading indicator stays forever
- No response

**Solutions:**
1. Check backend logs for errors
2. Verify LLM API key is valid
3. Check internet connection (LLM API needs internet)
4. Try different LLM provider

### Issue: Tool Calls Not Showing

**Symptoms:**
- Response appears but no tool indicators

**Solutions:**
1. Check browser console for errors
2. Verify ToolCallDisplay component exists
3. Check response format in Network tab

---

## Performance Testing

### Load Test Chat

**Test:**
Send 10 messages rapidly

**Expected:**
- All messages processed
- Responses appear in order
- No crashes or hangs

### Concurrent Users

**Test:**
Open multiple browser tabs, sign in as different users

**Expected:**
- Each user has separate conversation
- No cross-contamination
- All sessions work independently

---

## Browser Compatibility

Test in multiple browsers:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari

**Expected:**
- All features work
- UI renders correctly
- No browser-specific errors

---

## Mobile Testing

**Test:**
Open on mobile device or use browser dev tools mobile view

**Expected:**
- Responsive layout
- Chat interface usable
- Input field accessible
- Messages readable

---

## API Testing with cURL

### Send Chat Message

```bash
# First, get a token by signing in through the frontend
# Then use the token:

curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'
```

### Get Chat History

```bash
curl -X GET http://localhost:8000/api/{user_id}/chat/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Monitoring

### Backend Logs

Watch backend terminal for:
- Incoming requests
- LLM API calls
- Tool executions
- Errors

### Frontend Console

Watch browser console for:
- API calls (Network tab)
- React errors
- State updates

### Database

Check database for:
- New tasks created
- Conversation messages saved
- User sessions

---

## Success Criteria

All tests should pass:
- ✅ Backend starts without errors
- ✅ Frontend starts without errors
- ✅ User can register and sign in
- ✅ Chat interface loads
- ✅ Messages send and receive
- ✅ Tools execute correctly
- ✅ History persists
- ✅ Error handling works
- ✅ All chat commands work

---

## Next Steps After Testing

1. **Production Deployment**
   - Deploy backend to Railway/Render
   - Deploy frontend to Vercel/Netlify
   - Configure production environment variables

2. **Monitoring Setup**
   - Add logging service
   - Set up error tracking
   - Monitor LLM API usage

3. **Performance Optimization**
   - Add caching for LLM responses
   - Optimize database queries
   - Add rate limiting

4. **Feature Enhancements**
   - Add more agents
   - Implement more tools
   - Improve UI/UX

---

## Support

If you encounter issues:
1. Check this testing guide
2. Review backend/chatbot/README.md
3. Check frontend/CHATBOT_INTEGRATION.md
4. Review error logs
5. Test with cURL to isolate frontend/backend issues

---

**Testing Complete!** 🎉

If all tests pass, your TODO app with AI chatbot is fully functional and ready for use!
