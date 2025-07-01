<template>
  <main class="p-8 max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">📝 Task Scheduler</h1>

    <!-- Add Task Form -->
    <form @submit.prevent="createTask" class="mb-6 bg-gray-100 p-4 rounded">
      <input
        v-model="newTask.title"
        placeholder="Task title"
        class="p-2 border w-full mb-2"
        required
      />
      <textarea
        v-model="newTask.description"
        placeholder="Task description"
        class="p-2 border w-full mb-2"
      />
      <input
        v-model="newTask.due_date"
        type="datetime-local"
        class="p-2 border w-full mb-2"
      />
      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
        Add Task
      </button>
    </form>

    <!-- Task List -->
    <div v-if="tasks.length === 0" class="text-gray-500">No tasks yet.</div>
    <ul>
      <li
        v-for="task in tasks"
        :key="task.id"
        class="border p-4 mb-2 rounded bg-white shadow"
      >
        <h2 class="text-lg font-semibold">{{ task.title }}</h2>
        <p class="text-sm text-gray-700">{{ task.description }}</p>
        <p class="text-xs text-gray-500">Due: {{ formatDate(task.due_date) }}</p>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const tasks = ref([])
const newTask = ref({
  title: '',
  description: '',
  due_date: ''
})

// Load tasks from FastAPI
async function fetchTasks() {
  const res = await fetch('http://localhost:8000/tasks')
  tasks.value = await res.json()
}

// Create new task
async function createTask() {
  await fetch('http://localhost:8000/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newTask.value)
  })
  newTask.value = { title: '', description: '', due_date: '' }
  fetchTasks()
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString()
}

onMounted(fetchTasks)
</script>

<style>
body {
  font-family: system-ui, sans-serif;
  background: #f9fafb;
}
</style>
