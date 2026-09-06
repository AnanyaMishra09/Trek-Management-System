<script setup>
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiFetch } from "../../api";
import { auth, clearAuth } from "../../stores/auth";

const treks = ref([]);
const route = useRoute();
const router = useRouter();

async function load() {
  treks.value = await apiFetch("/api/staff/treks");
}
onMounted(load);
watch(
  () => route.path,
  (path) => {
    if (path === "/staff") load();
  }
);

function logout() {
  clearAuth();
  router.push("/login");
}
</script>

<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
    <span class="navbar-brand">⛰️Trekking Staff - {{ auth.name }}</span>
    <div class="navbar-nav me-auto">
      <router-link class="nav-link" to="/staff">My Treks</router-link>
    </div>
    <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
  </nav>

  <div class="container my-4">
    <div v-if="route.path === '/staff'" class="table-wrap">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Slots</th>
            <th>Registered</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in treks" :key="t.id">
            <td class="fw-medium">{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.slots }}</td>
            <td>{{ t.participant_count }}</td>
            <td>{{ t.status }}</td>
            <td>
              <router-link class="btn btn-sm btn-primary" :to="`/staff/treks/${t.id}`">Manage</router-link>
            </td>
          </tr>
          <tr v-if="!treks.length">
            <td colspan="6" class="text-center text-muted py-4">No treks assigned yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <router-view v-else />
  </div>
</template>
