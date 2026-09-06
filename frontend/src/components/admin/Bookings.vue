<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const bookings = ref([]);

const statusBadge = (s) => ({ Booked: "bg-success", Cancelled: "bg-danger", Completed: "bg-secondary" }[s] || "bg-secondary");

onMounted(async () => {
  bookings.value = await apiFetch("/api/history/bookings");
});
</script>

<template>
  <div class="table-wrap">
    <table class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Trek</th>
          <th>Trekker</th>
          <th>Email</th>
          <th>Booked At</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in bookings" :key="b.id">
          <td class="fw-medium">{{ b.trek.name }}</td>
          <td>{{ b.user.name }}</td>
          <td>{{ b.user.email }}</td>
          <td>{{ new Date(b.booked_at).toLocaleDateString() }}</td>
          <td><span class="badge" :class="statusBadge(b.status)">{{ b.status }}</span></td>
        </tr>
        <tr v-if="!bookings.length">
          <td colspan="5" class="text-center text-muted py-4">No bookings yet.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
