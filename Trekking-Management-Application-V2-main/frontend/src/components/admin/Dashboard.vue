<script setup>
import { nextTick, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiFetch } from "../../api";
import { auth, clearAuth } from "../../stores/auth";

const stats = ref(null);
const chartCanvas = ref(null);
const route = useRoute();
const router = useRouter();
let chart = null;

async function loadStats() {
  stats.value = await apiFetch("/api/admin/stats");
  await nextTick();
  renderChart();
}

function renderChart() {
  if (!chartCanvas.value || !stats.value) return;
  chart?.destroy();
  chart = new Chart(chartCanvas.value, {
    type: "bar",
    data: {
      labels: Object.keys(stats.value),
      datasets: [{ label: "Count", data: Object.values(stats.value), backgroundColor: "#0d6efd" }],
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
  });
}

onMounted(loadStats);
watch(
  () => route.path,
  (path) => {
    if (path === "/admin") nextTick(renderChart);
  }
);

function logout() {
  clearAuth();
  router.push("/login");
}
</script>

<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
    <span class="navbar-brand">⛰️Trekking Admin - {{ auth.name }}</span>
    <div class="navbar-nav me-auto">
      <router-link class="nav-link" to="/admin">Overview</router-link>
      <router-link class="nav-link" to="/admin/treks">Treks</router-link>
      <router-link class="nav-link" to="/admin/staff">Staff</router-link>
      <router-link class="nav-link" to="/admin/users">Users</router-link>
      <router-link class="nav-link" to="/admin/bookings">Bookings</router-link>
    </div>
    <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
  </nav>

  <div class="container my-4">
    <div v-if="route.path === '/admin'">
      <div class="row g-3 mb-4">
        <div class="col-3" v-for="(value, key) in stats" :key="key">
          <div class="card stat-tile text-center p-3">
            <div class="fs-3 fw-semibold">{{ value }}</div>
            <div class="text-muted text-capitalize small">{{ key }}</div>
          </div>
        </div>
      </div>
      <div class="card p-3">
        <canvas ref="chartCanvas" height="90"></canvas>
      </div>
    </div>
    <router-view v-else />
  </div>
</template>
