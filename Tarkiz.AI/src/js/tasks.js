class TaskManager {
  constructor() {
    this.tasks = [];
    this.taskInput = document.getElementById('taskInput');
    this.taskList = document.getElementById('taskList');
    this.addTaskButton = document.getElementById('addTask');
    this.taskCountDisplay = document.getElementById('taskCount');
    
    this.initializeEventListeners();
    this.loadTasks();
  }

  initializeEventListeners() {
    this.addTaskButton.addEventListener('click', () => this.addTask());
    this.taskInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.addTask();
    });
  }

  async loadTasks() {
    const data = await chrome.storage.sync.get(['tasks']);
    if (data.tasks) {
      this.tasks = data.tasks;
      this.renderTasks();
    }
  }

  async saveTasks() {
    await chrome.storage.sync.set({ tasks: this.tasks });
  }

  addTask() {
    const taskText = this.taskInput.value.trim();
    if (!taskText) return;

    const task = {
      id: Date.now(),
      text: taskText,
      completed: false,
      createdAt: new Date().toISOString()
    };

    this.tasks.unshift(task);
    this.taskInput.value = '';
    this.renderTasks();
    this.saveTasks();
  }

  toggleTask(taskId) {
    const task = this.tasks.find(t => t.id === taskId);
    if (task) {
      task.completed = !task.completed;
      this.renderTasks();
      this.saveTasks();
    }
  }

  deleteTask(taskId) {
    this.tasks = this.tasks.filter(t => t.id !== taskId);
    this.renderTasks();
    this.saveTasks();
  }

  renderTasks() {
    this.taskList.innerHTML = '';
    this.tasks.forEach(task => {
      const li = document.createElement('li');
      li.className = `task-item ${task.completed ? 'completed' : ''}`;
      
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = task.completed;
      checkbox.addEventListener('change', () => this.toggleTask(task.id));

      const text = document.createElement('span');
      text.textContent = task.text;

      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = '×';
      deleteBtn.className = 'delete-task';
      deleteBtn.addEventListener('click', () => this.deleteTask(task.id));

      li.appendChild(checkbox);
      li.appendChild(text);
      li.appendChild(deleteBtn);
      this.taskList.appendChild(li);
    });

    const completedCount = this.tasks.filter(t => t.completed).length;
    this.taskCountDisplay.textContent = completedCount;
  }
}

new TaskManager();