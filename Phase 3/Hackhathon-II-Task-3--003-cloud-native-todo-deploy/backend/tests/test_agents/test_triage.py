"""
Unit tests for triage agent routing

Per Constitution Principle V: Test-First (NON-NEGOTIABLE)
Tests that user messages are routed to the correct specialist agent.
"""
import pytest
from chatbot.agents.triage import get_agent_for_message
from chatbot.agents.task_agent import task_agent
from chatbot.agents.tag_agent import tag_agent
from chatbot.agents.reminder_agent import reminder_agent
from chatbot.agents.analytics_agent import analytics_agent


def test_route_to_task_agent_add():
    """Test routing 'add task' messages to task agent"""
    agent = get_agent_for_message("Add a task to buy groceries")
    assert agent == task_agent


def test_route_to_task_agent_list():
    """Test routing 'list tasks' messages to task agent"""
    agent = get_agent_for_message("Show my tasks")
    assert agent == task_agent


def test_route_to_task_agent_update():
    """Test routing 'update task' messages to task agent"""
    agent = get_agent_for_message("Update task 5 to buy organic groceries")
    assert agent == task_agent


def test_route_to_task_agent_complete():
    """Test routing 'complete task' messages to task agent"""
    agent = get_agent_for_message("Mark task 3 as done")
    assert agent == task_agent


def test_route_to_task_agent_delete():
    """Test routing 'delete task' messages to task agent"""
    agent = get_agent_for_message("Delete task 2")
    assert agent == task_agent


def test_route_to_tag_agent_add():
    """Test routing 'add tag' messages to tag agent"""
    agent = get_agent_for_message("Tag task 1 with urgent")
    assert agent == tag_agent


def test_route_to_tag_agent_remove():
    """Test routing 'remove tag' messages to tag agent"""
    agent = get_agent_for_message("Remove tag urgent from task 1")
    assert agent == tag_agent


def test_route_to_tag_agent_list():
    """Test routing 'list tags' messages to tag agent"""
    agent = get_agent_for_message("Show my tags")
    assert agent == tag_agent


def test_route_to_tag_agent_filter():
    """Test routing 'filter by tag' messages to tag agent"""
    agent = get_agent_for_message("Show tasks with tag work")
    assert agent == tag_agent


def test_route_to_reminder_agent_schedule():
    """Test routing 'schedule reminder' messages to reminder agent"""
    agent = get_agent_for_message("Remind me about task 1 tomorrow at 9am")
    assert agent == reminder_agent


def test_route_to_reminder_agent_cancel():
    """Test routing 'cancel reminder' messages to reminder agent"""
    agent = get_agent_for_message("Cancel my reminder for task 1")
    assert agent == reminder_agent


def test_route_to_reminder_agent_list():
    """Test routing 'list reminders' messages to reminder agent"""
    agent = get_agent_for_message("Show my reminders")
    assert agent == reminder_agent


def test_route_to_analytics_agent_count():
    """Test routing 'count tasks' messages to analytics agent"""
    agent = get_agent_for_message("How many tasks do I have?")
    assert agent == analytics_agent


def test_route_to_analytics_agent_done():
    """Test routing 'tasks done' messages to analytics agent"""
    agent = get_agent_for_message("How many tasks are completed?")
    assert agent == analytics_agent


def test_route_to_analytics_agent_pending():
    """Test routing 'tasks pending' messages to analytics agent"""
    agent = get_agent_for_message("How many tasks are pending?")
    assert agent == analytics_agent


def test_default_to_task_agent():
    """Test that ambiguous messages default to task agent"""
    agent = get_agent_for_message("What can you do?")
    assert agent == task_agent


def test_case_insensitive_routing():
    """Test that routing is case-insensitive"""
    agent1 = get_agent_for_message("ADD TASK buy milk")
    agent2 = get_agent_for_message("add task buy milk")
    assert agent1 == agent2 == task_agent


def test_partial_keyword_matching():
    """Test that partial keywords are matched"""
    agent = get_agent_for_message("I need to add a new task")
    assert agent == task_agent


def test_priority_when_multiple_keywords():
    """Test routing priority when message contains multiple keywords"""
    # "tag" keyword should take priority over "task"
    agent = get_agent_for_message("Add tag urgent to my task")
    assert agent == tag_agent
