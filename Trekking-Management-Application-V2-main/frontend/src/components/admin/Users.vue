<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const users = ref([]);
const q = ref("");

async function load() {
  users.value = await apiFetch(`/api/admin/users${q.value ? `?q=${encodeURIComponent(q.value)}` : ""}`);
}
onMounted(load);

async function toggle(user) {
  await apiFetch(`/api/admin/users/${user.id}/toggle-active`, { method: "PATCH" });
  await load();
}
</script>

<template>
  <input v-model="q" @keyup.enter="load" class="form-control w-auto mb-3" placeholder="Search by name/email" />

  <div class="table-wrap">
    <table class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td class="fw-medium">{{ u.name }}</td>
          <td>{{ u.email }}</td>
          <td>
            <span :class="u.is_active ? 'badge bg-success' : 'badge bg-danger'">
              {{ u.is_active ? "Active" : "Blacklisted" }}
            </span>
          </td>
          <td>
            <button class="btn btn-sm" :class="u.is_active ? 'btn-danger' : 'btn-success'" @click="toggle(u)">
              {{ u.is_active ? "Blacklist" : "Reinstate" }}
            </button>
          </td>
        </tr>
        <tr v-if="!users.length">
          <td colspan="4" class="text-center text-muted py-4">No trekkers yet.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
