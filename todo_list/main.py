import click
import json
import os

# 👇 OOP Concept: Encapsulation
# All the logic for managing tasks is inside this class
class TodoManager:
    def __init__(self, file_name="todo.json"):
        self.file_name = file_name  # Save file name for storing tasks

    # 👇 OOP Concept: Abstraction
    # This method hides the details of reading from a file
    def load_tasks(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as file:
                    return json.load(file)  # Load task list
            except json.JSONDecodeError:
                return []
        return []

    # This method hides the details of saving to a file
    def save_tasks(self, tasks):
        with open(self.file_name, "w") as file:
            json.dump(tasks, file, indent=4)

    # Add a new task
    def add_task(self, task):
        tasks = self.load_tasks()
        tasks.append({"task": task, "done": False})  # Add new task with "not done" status
        self.save_tasks(tasks)
        return task

    # Show all tasks
    def list_tasks(self):
        return self.load_tasks()

    # Mark a task as completed
    def complete_task(self, task_number):
        tasks = self.load_tasks()
        if 0 < task_number <= len(tasks):
            tasks[task_number - 1]["done"] = True
            self.save_tasks(tasks)
            return True
        return False

    # Delete a task
    def delete_task(self, task_number):
        tasks = self.load_tasks()
        if 0 < task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            self.save_tasks(tasks)
            return removed_task["task"]
        return None

# CLI (Command Line Interface) starts here
@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

# Create an object of TodoManager
manager = TodoManager()

@cli.command()
@click.argument("task")
def add(task):
    """Add a new task to the list"""
    manager.add_task(task)
    click.echo(f"✅ Task added: {task}")

@cli.command(name="list")
def list_tasks():
    """List all tasks"""
    tasks = manager.list_tasks()
    if not tasks:
        click.echo("📭 No Task Found")
        return
    for index, task in enumerate(tasks):
        status = "✅ Done" if task["done"] else "⏳ Not Done"
        click.echo(f"{index + 1}. {task['task']} - {status}")

@cli.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as complete"""
    success = manager.complete_task(task_number)
    if success:
        click.echo(f"✅ Task {task_number} marked as completed")
    else:
        click.echo("❌ Invalid Task Number")

@cli.command()
@click.argument("task_number", type=int)
def delete(task_number):
    """Delete a task"""
    removed = manager.delete_task(task_number)
    if removed:
        click.echo(f"🗑️ Task '{removed}' deleted")
    else:
        click.echo("❌ Invalid Task Number")

# Start the CLI application
if __name__ == "__main__":
    cli()
