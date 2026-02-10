from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from ..database.session import get_db_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..dependencies.auth import get_current_user_id, verify_user_id_match_path
from ..schemas.responses import BaseResponse
from fastapi import Path

router = APIRouter(prefix="/api")

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_user_tasks(
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Get all tasks for a specific user
    """
    # Verify that the current user ID matches the path user ID
    verify_user_id_match_path(user_id, current_user_id)

    # Now get the tasks for the user
    tasks = await TaskService.get_tasks_by_user_id(user_id, db_session)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Create a task for a specific user
    """
    # Verify that the current user ID matches the path user ID
    verify_user_id_match_path(user_id, current_user_id)

    # Now create the task for the user
    task = await TaskService.create_task_for_user(task_data, user_id, db_session)
    return task


@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
async def get_task(
    id: str = Path(..., description="Task ID"),
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific task for a specific user
    """
    # Verify that the current user ID matches the path user ID
    verify_user_id_match_path(user_id, current_user_id)

    # Now get the specific task for the user
    task = await TaskService.get_task_by_id_and_user_id(id, user_id, db_session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
async def update_task(
    task_data: TaskUpdate,
    id: str = Path(..., description="Task ID"),
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific task for a specific user
    """
    # Verify that the current user ID matches the path user ID
    verify_user_id_match_path(user_id, current_user_id)

    # Now update the task for the user
    task = await TaskService.update_task_for_user(id, task_data, user_id, db_session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return task


@router.delete("/{user_id}/tasks/{id}")
async def delete_task(
    id: str = Path(..., description="Task ID"),
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific task for a specific user
    """
    # Verify that the current user ID matches the path user ID
    verify_user_id_match_path(user_id, current_user_id)

    # Now delete the task for the user
    deleted = await TaskService.delete_task_for_user(id, user_id, db_session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return {"success": True, "message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
async def update_task_completion(
    completed: dict,
    id: str = Path(..., description="Task ID"),
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Update the completion status of a specific task for a specific user
    """
    # Verify that the current user ID matches the path user ID
    verify_user_id_match_path(user_id, current_user_id)

    # Now update the task completion status for the user
    completed_status = completed.get("completed", False)
    task = await TaskService.update_task_completion_for_user(id, completed_status, user_id, db_session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return task