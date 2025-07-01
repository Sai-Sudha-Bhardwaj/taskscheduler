<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Task Scheduler</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="dialogs.login = true" v-if="!isAuthenticated">Login</v-btn>
      <v-btn text @click="logout" v-else>Logout</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-card class="mb-4">
          <v-card-title>Create New Task</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="newTask.title"
              label="Task Title"
              outlined
              dense
            ></v-text-field>
            <v-text-field
              v-model="newTask.description"
              label="Description (Optional)"
              outlined
              dense
            ></v-text-field>
            <v-text-field
              v-model="newTask.due_date"
              label="Due Date (YYYY-MM-DD HH:MM:SS)"
              outlined
              dense
            ></v-text-field>
            <v-btn color="success" @click="createTask" :disabled="!isAuthenticated || !newTask.title">Add Task</v-btn>
          </v-card-text>
        </v-card>

        <v-card>
          <v-card-title>
            All Tasks
            <v-spacer></v-spacer>
            <v-btn icon @click="fetchTasks">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item v-if="tasks.length === 0">
                <v-list-item-content>
                  <v-list-item-title>No tasks available. Create one!</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <template v-for="(task, index) in tasks" :key="task.id">
                <v-list-item>
                  <v-list-item-action>
                    <v-checkbox
                      v-model="task.completed"
                      @change="updateTaskStatus(task)"
                      :disabled="!isAuthenticated"
                    ></v-checkbox>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title :class="{ 'text-decoration-line-through': task.completed }">
                      {{ task.title }}
                    </v-list-item-title>
                    <v-list-item-subtitle>{{ task.description }}</v-list-item-subtitle>
                    <v-list-item-subtitle>Due: {{ formatDate(task.due_date) }}</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn icon @click="editTask(task)" :disabled="!isAuthenticated">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </v-list-item-action>
                  <v-list-item-action>
                    <v-btn icon @click="confirmDelete(task.id)" :disabled="!isAuthenticated">
                      <v-icon color="error">mdi-delete</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
                <v-divider v-if="index < tasks.length - 1"></v-divider>
              </template>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>

    <v-dialog v-model="dialogs.login" max-width="500px">
      <v-card>
        <v-card-title class="headline">Login</v-card-title>
        <v-card-text>
          <v-text-field v-model="loginForm.email" label="Email" type="email" required></v-text-field>
          <v-text-field v-model="loginForm.password" label="Password" type="password" required></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialogs.login = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="login">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogs.edit" max-width="500px">
      <v-card>
        <v-card-title class="headline">Edit Task</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="editedTask.title"
            label="Task Title"
            outlined
            dense
          ></v-text-field>
          <v-text-field
            v-model="editedTask.description"
            label="Description (Optional)"
            outlined
            dense
          ></v-text-field>
          <v-text-field
            v-model="editedTask.due_date"
            label="Due Date (YYYY-MM-DD HH:MM:SS)"
            outlined
            dense
          ></v-text-field>
          <v-checkbox
            v-model="editedTask.completed"
            label="Completed"
          ></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialogs.edit = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveEditedTask">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogs.confirmDelete" max-width="300px">
      <v-card>
        <v-card-title class="headline">Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete this task?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialogs.confirmDelete = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteTask(taskToDeleteId)">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn text @click="snackbar.show = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import moment from 'moment'; // Make sure you have installed moment: npm install moment

// Configuration
const BACKEND_URL = 'http://localhost:8000'; // Your FastAPI backend URL

// Reactive data
const tasks = ref([]);
const newTask = ref({
  title: '',
  description: '',
  due_date: moment().add(1, 'day').format('YYYY-MM-DD HH:mm:ss'), // Default to tomorrow
});
const editedTask = ref({});
const taskToDeleteId = ref(null);

const dialogs = ref({
  login: false,
  edit: false,
  confirmDelete: false,
});

const snackbar = ref({
  show: false,
  message: '',
  color: 'success',
  timeout: 3000,
});

const loginForm = ref({
  email: '',
  password: '',
});

const token = ref(localStorage.getItem('access_token') || null);

// Computed property for authentication status
const isAuthenticated = computed(() => !!token.value);

// Axios instance with token
const axiosInstance = axios.create({
  baseURL: BACKEND_URL,
});

axiosInstance.interceptors.request.use(
  (config) => {
    if (token.value) {
      config.headers.Authorization = `Bearer ${token.value}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle token expiration or invalid token
    if (error.response && error.response.status === 401) {
      logout(); // Log out user if token is invalid/expired
      showSnackbar('Session expired or unauthorized. Please log in again.', 'error');
    }
    return Promise.reject(error);
  }
);

// --- Methods ---

const showSnackbar = (message, color = 'success', timeout = 3000) => {
  snackbar.value.show = true;
  snackbar.value.message = message;
  snackbar.value.color = color;
  snackbar.value.timeout = timeout;
};

const formatDate = (dateString) => {
  return moment(dateString).format('MMMM Do YYYY, h:mm:ss a');
};

// --- Authentication Methods ---
const login = async () => {
  try {
    const formData = new FormData();
    formData.append('username', loginForm.value.email);
    formData.append('password', loginForm.value.password);

    const response = await axiosInstance.post('/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    token.value = response.data.access_token;
    localStorage.setItem('access_token', token.value);
    dialogs.value.login = false;
    loginForm.value = { email: '', password: '' }; // Clear form
    showSnackbar('Logged in successfully!', 'success');
    fetchTasks(); // Fetch tasks after login
  } catch (error) {
    console.error('Login error:', error.response?.data || error.message);
    showSnackbar(`Login failed: ${error.response?.data?.detail || 'Unknown error'}`, 'error');
  }
};

const logout = () => {
  token.value = null;
  localStorage.removeItem('access_token');
  tasks.value = []; // Clear tasks on logout
  showSnackbar('Logged out successfully!', 'info');
};

// --- Task CRUD Methods ---

const fetchTasks = async () => {
  if (!isAuthenticated.value) {
    tasks.value = [];
    showSnackbar('Please log in to view tasks.', 'info');
    return;
  }
  try {
    const response = await axiosInstance.get('/tasks/');
    tasks.value = response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error.response?.data || error.message);
    showSnackbar(`Failed to fetch tasks: ${error.response?.data?.detail || 'Unknown error'}`, 'error');
  }
};

const createTask = async () => {
  if (!newTask.value.title) {
    showSnackbar('Task title cannot be empty!', 'warning');
    return;
  }
  try {
    const response = await axiosInstance.post('/tasks/', newTask.value);
    showSnackbar('Task created successfully!', 'success');
    newTask.value = {
      title: '',
      description: '',
      due_date: moment().add(1, 'day').format('YYYY-MM-DD HH:mm:ss'),
    }; // Reset form
    fetchTasks(); // Refresh tasks
  } catch (error) {
    console.error('Error creating task:', error.response?.data || error.message);
    showSnackbar(`Failed to create task: ${error.response?.data?.detail || 'Unknown error'}`, 'error');
  }
};

const updateTaskStatus = async (task) => {
  try {
    await axiosInstance.put(`/tasks/${task.id}`, {
      title: task.title,
      description: task.description,
      due_date: task.due_date, // Send original due_date
      completed: task.completed,
    });
    showSnackbar('Task status updated!', 'success');
  } catch (error) {
    console.error('Error updating task status:', error.response?.data || error.message);
    // Revert checkbox state if update fails
    task.completed = !task.completed;
    showSnackbar(`Failed to update task status: ${error.response?.data?.detail || 'Unknown error'}`, 'error');
  }
};

const editTask = (task) => {
  editedTask.value = { ...task }; // Create a copy to edit
  dialogs.value.edit = true;
};

const saveEditedTask = async () => {
  try {
    await axiosInstance.put(`/tasks/${editedTask.value.id}`, editedTask.value);
    showSnackbar('Task updated successfully!', 'success');
    dialogs.value.edit = false;
    fetchTasks(); // Refresh tasks
  } catch (error) {
    console.error('Error saving edited task:', error.response?.data || error.message);
    showSnackbar(`Failed to save task: ${error.response?.data?.detail || 'Unknown error'}`, 'error');
  }
};

const confirmDelete = (taskId) => {
  taskToDeleteId.value = taskId;
  dialogs.value.confirmDelete = true;
};

const deleteTask = async (taskId) => {
  try {
    await axiosInstance.delete(`/tasks/${taskId}`);
    showSnackbar('Task deleted successfully!', 'success');
    dialogs.value.confirmDelete = false;
    taskToDeleteId.value = null; // Clear ID
    fetchTasks(); // Refresh tasks
  } catch (error) {
    console.error('Error deleting task:', error.response?.data || error.message);
    showSnackbar(`Failed to delete task: ${error.response?.data?.detail || 'Unknown error'}`, 'error');
  }
};

// --- Lifecycle Hook ---
onMounted(() => {
  if (isAuthenticated.value) {
    fetchTasks(); // Fetch tasks if already logged in on mount
  }
});
</script>

<style scoped>
/* Optional: Add custom styles here if needed */
.text-decoration-line-through {
  text-decoration: line-through;
}
</style>