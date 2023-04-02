<template>
  <div id="app" class="app-container">
    <div class="form-container">
      <h1 class="main-title">TODO App</h1>
      <form @submit.prevent="addTodo" class="form">
        <div class="form-group">
          <input v-model="newTodo.title" placeholder="Title" class="input" />
        </div>
        <div class="form-group">
          <input v-model="newTodo.deadline" type="datetime-local" placeholder="Deadline" class="input" />
        </div>
        <div class="form-group">
          <input v-model="newTodo.status" placeholder="Status" class="input" disabled />
        </div>
        <button type="submit" class="submit-button">Add TODO</button>
      </form>
      <form v-if="editMode" @submit.prevent="updateTodo" class="form">
        <div class="form-group">
          <input v-model="currentTodo.title" placeholder="Title" class="input" />
        </div>
        <div class="form-group">
          <input v-model="currentTodo.deadline" type="datetime-local" placeholder="Deadline" class="input" />
        </div>
        <div class="form-group">
          <input v-model="currentTodo.status" placeholder="Status" class="input" disabled />
        </div>
        <button type="submit" class="update-button">Update TODO</button>
      </form>
      <ul>
        <li v-for="todo in todos" :key="todo.id" class="todo-item">
          <div class="todo-title">{{ todo.title }}</div>
          <div class="todo-deadline">{{ todo.deadline }}</div>
          <div :class="{'status-overdue': todo.status == 'Overdue', 'status-due-soon': todo.status == 'Due Soon', 'status-completed': todo.status == 'Completed'}" class="status">{{ todo.status }}</div>
          <div>
            <button @click="editTodo(todo)" class="edit-button">Edit</button>
            <button @click="deleteTodo(todo.id)" class="delete-button">Delete</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      newTodo: {
        id: null,
        title: '',
        deadline: '',
        status: '',
        start_time: null,
        end_time: null,
        time_spent: null,
        reminders: [],
      },
      currentTodo: null,
      editMode: false,
    };
  },
  async created() {
    await this.getTodos();
  },
  methods: {
    async getTodos() {
      const response = await axios.get('/todo/');
      this.todos = response.data;
    },
    async addTodo() {
      this.newTodo.id = Date.now();
      await axios.post('/todo/', this.newTodo);
      this.todos.push({ ...this.newTodo });
      this.newTodo.title = '';
      this.newTodo.deadline = 
      this.newTodo.status = '';
    },
    async updateTodo() {
      await axios.put(`/todo/${this.currentTodo.id}`, this.currentTodo);
      const index = this.todos.findIndex((todo) => todo.id === this.currentTodo.id);
      this.todos[index] = { ...this.currentTodo };
      this.editMode = false;
    },
    async deleteTodo(id) {
      await axios.delete(`/todo/${id}`);
      this.todos = this.todos.filter((todo) => todo.id !== id);
    },
    editTodo(todo) {
      this.currentTodo = { ...todo };
      this.editMode = true;
    },
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
}

/* app.css */
.app-container {
  min-height: 100vh;
  background-color: #F7FAFC;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-container {
  position: relative;
  padding: 1rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.main-title {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
}

.form {
  background-color: white;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  border-radius: 0.375rem;
  padding-left: 2rem;
  padding-top: 1.5rem;
  padding-bottom: 2rem;
  padding-right: 2rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.input {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  appearance: none;
  border: 1px solid #E2E8F0;
  border-radius: 0.375rem;
  width: 100%;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #4A5568;
}

.submit-button,
.update-button {
  width: 100%;
  background-color: #4299E1;
  color: white;
  font-weight: 700;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  padding-left: 1rem;
  padding-right: 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
}

.update-button {
  background-color: #48BB78;
}

.submit-button:hover,
.update-button:hover {
  opacity: 0.9;
}

.todo-item {
  background-color: white;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  border-radius: 0.375rem;
  margin-bottom: 1rem;
  padding: 1rem;
}

.todo-title {
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.todo-deadline {
  margin-bottom: 0.5rem;
}

.status {
  display: inline-block;
  border-radius: 9999px;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
}

.status-overdue {
  background-color: #E53E3E;
}

.status-due-soon {
  background-color: #ECC94B;
}

.status-completed {
  background-color: #38A169;
}

.edit-button,
.delete-button {
  background-color: #4299E1;
  color: white;
  font-weight: 700;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  margin-right: 0.5rem;
}

.delete-button {
  background-color: #E53E3E;
}

.edit-button:hover,
.delete-button:hover {
  opacity: 0.9;
}


</style>
