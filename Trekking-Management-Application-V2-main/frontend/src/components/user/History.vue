<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";
import { auth } from "../../stores/auth";

const bookings = ref([]);
const exporting = ref(false);
const exportError = ref("");
const exportDone = ref(false);

const statusBadge = (s) => ({ Booked: "bg-success", Cancelled: "bg-danger", Completed: "bg-secondary" }[s] || "bg-secondary");
const trekStatusBadge = (s) =>
  ({ Open: "bg-success", Started: "bg-warning", Completed: "bg-secondary", Closed: "bg-dark" }[s] || "bg-secondary");

async function load() {
  bookings.value = await apiFetch("/api/history/bookings");
}
onMounted(load);

async function cancel(b) {
  if (!confirm(`Cancel booking for "${b.trek.name}"?`)) return;
  await apiFetch(`/api/history/bookings/${b.id}/cancel`, { method: "POST" });
  await load();
}

async function exportCsv() {
  exporting.value = true;
  exportError.value = "";
  exportDone.value = false;
  try {
    const { task_id } = await apiFetch("/api/export/booking-history", { method: "POST" });

    let status = "PENDING";
    while (status !== "SUCCESS") {
      await new Promise((r) => setTimeout(r, 800));
      ({ status } = await apiFetch(`/api/export/booking-history/${task_id}`));
      if (status === "FAILURE") throw new Error("export failed");
    }

    const res = await fetch(`/api/export/booking-history/${task_id}/download`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "booking_history.csv";
    a.click();
    URL.revokeObjectURL(url);
    exportDone.value = true;
  } catch (e) {
    exportError.value = e.message;
  } finally {
    exporting.value = false;
  }
}
</script>

<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1 class="h4 mb-0">Booking History</h1>
    <button class="btn btn-outline-secondary btn-sm" :disabled="exporting" @click="exportCsv">
      {{ exporting ? "Exporting..." : "Export CSV" }}
    </button>
  </div>
  <div v-if="exportDone" class="alert alert-success alert-dismissible" role="alert">
    Export complete — your booking history CSV has downloaded.
    <button type="button" class="btn-close" @click="exportDone = false"></button>
  </div>
  <p v-if="exportError" class="text-danger">{{ exportError }}</p>

  <div class="table-wrap">
    <table class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Trek</th>
          <th>Location</th>
          <th>Booked At</th>
          <th>Booking</th>
          <th>Trek Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in bookings" :key="b.id">
          <td class="fw-medium">{{ b.trek.name }}</td>
          <td>{{ b.trek.location }}</td>
          <td>{{ new Date(b.booked_at).toLocaleDateString() }}</td>
          <td>
            <span class="badge" :class="statusBadge(b.status)">{{ b.status }}</span>
            <div v-if="b.status === 'Cancelled' && b.cancel_reason" class="small text-muted">{{ b.cancel_reason }}</div>
          </td>
          <td><span class="badge" :class="trekStatusBadge(b.trek.status)">{{ b.trek.status }}</span></td>
          <td>
            <button v-if="b.status === 'Booked'" class="btn btn-sm btn-danger" @click="cancel(b)">Cancel</button>
          </td>
        </tr>
        <tr v-if="!bookings.length">
          <td colspan="6" class="text-center text-muted py-4">No bookings yet.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
