<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4">Your Tasks</h1>
      </v-col>
    </v-row>

    <v-row class="mb-4">
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-title class="text-h5">{{ editingTask ? 'Edit Task' : 'Add New Task' }}</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="saveTask">
              <v-text-field
                v-model="newTask.title"
                label="Task Title"
                required
                :rules="[v => !!v || 'Title is required']"
              ></v-text-field>
              <v-textarea
                v-model="newTask.description"
                label="Description (Optional)"
                rows="2"
              ></v-textarea>

              <v-menu
                v-model="datePickerMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="formattedDueDate"
                    label="Due Date (Optional)"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    clearable
                    @click:clear="newTask.due_date = null"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="selectedDate"
                  @input="datePickerMenu = false"
                ></v-date-picker>
              </v-menu>

              <v-checkbox
                v-if="editingTask"
                v-model="newTask.completed"
                label="Completed"
              ></v-checkbox>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" type="submit" :loading="loading">
                  {{ editingTask ? 'Update Task' : 'Add Task' }}
                </v-btn>
                <v-btn v-if="editingTask" color="warning" @click="cancelEdit">Cancel Edit</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            Tasks
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="filteredTasks"
            :search="search"
            :loading="loadingTasks"
            class="elevation-1"
          >
            <template v-slot:item.due_date="{ item }">
              {{ item.due_date ? new Date(item.due_date).toLocaleDateString() : 'N/A' }}
            </template>
            <template v-slot:item.completed="{ item }">
              <v-icon :color="item.completed ? 'success' : 'error'">
                {{ item.completed ? 'mdi-check-circle' : 'mdi-close-circle' }}
              </v-icon>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="editTask(item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="deleteTask(item.id)">
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:no-data>
              <v-btn color="primary" @click="fetchTasks">Reset</v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbar.show = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment'; // For date formatting

export default {
  name: 'TaskView',
  data() {
    return {
      search: '',
      headers: [
        { title: 'Title', align: 'start', key: 'title' },
        { title: 'Description', key: 'description' },
        { title: 'Due Date', key: 'due_date' },
        { title: 'Completed', key: 'completed' },
        { title: 'Actions', key: 'actions', sortable: false },
      ],
      tasks: [],
      filteredTasks: [], // For computed property if more complex filtering is needed
      newTask: {
        title: '',
        description: '',
        due_date: null,
        completed: false,
      },
      editingTask: null, // Stores the task being edited
      loading: false, // For form submission loading state
      loadingTasks: false, // For task list loading state
      datePickerMenu: false, // For the date picker visibility
      selectedDate: null, // Date model for the date picker
      snackbar: {
        show: false,
        message: '',
        color: '',
      },
    };
  },
  computed: {
    formattedDueDate: {
      get() {
        return this.newTask.due_date ? moment(this.newTask.due_date).format('YYYY-MM-DD') : '';
      },
      set(val) {
        // This setter is needed for v-text-field to function,
        // but the date picker itself sets selectedDate
        // We handle the actual newTask.due_date update via selectedDate watcher
      }
    }
  },
  watch: {
    selectedDate(newDate) {
      if (newDate) {
        // Convert selectedDate (YYYY-MM-DD) to ISO string for backend
        this.newTask.due_date = moment(newDate).toISOString();
      } else {
        this.newTask.due_date = null;
      }
    },
    tasks: {
      handler(newTasks) {
        this.filteredTasks = newTasks; // Simple filtering for now
      },
      deep: true,
      immediate: true
    }
  },
  async created() {
    await this.fetchTasks();
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('access_token');
      return {
        Authorization: `Bearer ${token}`,
      };
    },
    showSnackbar(message, color = 'success') {
      this.snackbar.message = message;
      this.snackbar.color = color;
      this.snackbar.show = true;
    },
    async fetchTasks() {
      this.loadingTasks = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/tasks/', {
          headers: this.getAuthHeaders(),
        });
        this.tasks = response.data;
      } catch (err) {
        console.error('Error fetching tasks:', err);
        if (err.response && err.response.status === 401) {
          this.showSnackbar('Session expired or unauthorized. Please log in.', 'error');
          this.$router.push('/login');
        } else {
          this.showSnackbar('Failed to fetch tasks.', 'error');
        }
      } finally {
        this.loadingTasks = false;
      }
    },
    async saveTask() {
      this.loading = true;
      try {
        if (this.editingTask) {
          // Update existing task
          const response = await axios.put(`http://127.0.0.1:8000/tasks/${this.editingTask.id}`, this.newTask, {
            headers: this.getAuthHeaders(),
          });
          this.showSnackbar('Task updated successfully!');
          console.log('Task updated:', response.data);
        } else {
          // Create new task
          const response = await axios.post('http://127.0.0.1:8000/tasks/', this.newTask, {
            headers: this.getAuthHeaders(),
          });
          this.showSnackbar('Task added successfully!');
          console.log('Task added:', response.data);
        }
        await this.fetchTasks(); // Refresh list
        this.resetForm();
      } catch (err) {
        console.error('Error saving task:', err.response?.data || err);
        this.showSnackbar(`Failed to save task: ${err.response?.data?.detail || err.message}`, 'error');
      } finally {
        this.loading = false;
      }
    },
    editTask(task) {
      this.editingTask = { ...task }; // Create a copy to avoid direct mutation
      this.newTask = { ...task }; // Populate form with task data
      // Ensure date picker model is correctly set for editing
      this.selectedDate = task.due_date ? moment(task.due_date).format('YYYY-MM-DD') : null;
    },
    cancelEdit() {
      this.resetForm();
    },
    async deleteTask(id) {
      if (confirm('Are you sure you want to delete this task?')) {
        try {
          await axios.delete(`http://127.0.0.1:8000/tasks/${id}`, {
            headers: this.getAuthHeaders(),
          });
          this.showSnackbar('Task deleted successfully!');
          await this.fetchTasks(); // Refresh list
        } catch (err) {
          console.error('Error deleting task:', err);
          this.showSnackbar('Failed to delete task.', 'error');
        }
      }
    },
    resetForm() {
      this.newTask = {
        title: '',
        description: '',
        due_date: null,
        completed: false,
      };
      this.editingTask = null;
      this.selectedDate = null;
      this.datePickerMenu = false;
    },
  },
};
</script>

<style scoped>
/* Add any specific styles for this component here */
</style>