<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const treks = ref([]);
const q = ref("");
const editing = ref(null);
const showModal = ref(false);
const staffList = ref([]);
const error = ref("");
const validated = ref(false);

const empty = () => ({ name: "", location: "", difficulty: "", duration_days: null, price: null, slots: null });
const form = ref(empty());

const difficultyBadge = (d) => ({ Easy: "badge-easy", Moderate: "badge-moderate", Hard: "badge-hard" }[d] || "bg-secondary");

async function load() {
  treks.value = await apiFetch(`/api/admin/treks${q.value ? `?q=${encodeURIComponent(q.value)}` : ""}`);
}

onMounted(async () => {
  await load();
  staffList.value = await apiFetch("/api/admin/staff");
});

function openCreate() {
  editing.value = null;
  form.value = empty();
  error.value = "";
  validated.value = false;
  showModal.value = true;
}

function openEdit(trek) {
  editing.value = trek;
  form.value = { ...trek };
  error.value = "";
  validated.value = false;
  showModal.value = true;
}

async function onSubmit(e) {
  validated.value = true;
  if (!e.target.checkValidity()) return;
  await save();
}

async function save() {
  try {
    if (editing.value) {
      await apiFetch(`/api/admin/treks/${editing.value.id}`, { method: "PUT", body: JSON.stringify(form.value) });
    } else {
      await apiFetch("/api/admin/treks", { method: "POST", body: JSON.stringify(form.value) });
    }
    showModal.value = false;
    await load();
  } catch (e) {
    error.value = e.message;
  }
}

async function remove(trek) {
  if (!confirm(`Delete trek "${trek.name}"?`)) return;
  await apiFetch(`/api/admin/treks/${trek.id}`, { method: "DELETE" });
  await load();
}

async function assign(trek, event) {
  const staff_id = event.target.value || null;
  await apiFetch(`/api/admin/treks/${trek.id}/assign`, { method: "PATCH", body: JSON.stringify({ staff_id }) });
  await load();
}
</script>

<template>
  <div class="d-flex justify-content-between mb-3">
    <input v-model="q" @keyup.enter="load" class="form-control w-auto" placeholder="Search by name/location" />
    <button class="btn btn-primary" @click="openCreate">+ New Trek</button>
  </div>

  <div class="table-wrap">
    <table class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Name</th>
          <th>Location</th>
          <th>Difficulty</th>
          <th>Days</th>
          <th>Price</th>
          <th>Slots</th>
          <th>Status</th>
          <th>Staff</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in treks" :key="t.id">
          <td class="fw-medium">{{ t.name }}</td>
          <td>{{ t.location }}</td>
          <td><span class="badge" :class="difficultyBadge(t.difficulty)">{{ t.difficulty }}</span></td>
          <td>{{ t.duration_days }}</td>
          <td>₹{{ t.price }}</td>
          <td>{{ t.slots }}</td>
          <td>{{ t.status }}</td>
          <td>
            <select class="form-select form-select-sm" :value="t.staff_id ?? ''" @change="assign(t, $event)">
              <option value="">Unassigned</option>
              <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </td>
          <td>
            <button class="btn btn-sm btn-secondary me-1" @click="openEdit(t)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="remove(t)">Delete</button>
          </td>
        </tr>
        <tr v-if="!treks.length">
          <td colspan="9" class="text-center text-muted py-4">No treks yet.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ editing ? "Edit Trek" : "New Trek" }}</h5>
          <button type="button" class="btn-close" @click="showModal = false"></button>
        </div>
        <form class="modal-body" novalidate :class="{ 'was-validated': validated }" @submit.prevent="onSubmit">
          <div class="mb-2">
            <input class="form-control" v-model="form.name" placeholder="Name" required />
            <div class="invalid-feedback">Name is required.</div>
          </div>
          <div class="mb-2">
            <input class="form-control" v-model="form.location" placeholder="Location" required />
            <div class="invalid-feedback">Location is required.</div>
          </div>
          <div class="mb-2">
            <select class="form-select" v-model="form.difficulty" required>
              <option value="" disabled>Select difficulty</option>
              <option>Easy</option>
              <option>Moderate</option>
              <option>Hard</option>
            </select>
            <div class="invalid-feedback">Difficulty is required.</div>
          </div>
          <div class="mb-2">
            <input class="form-control" type="number" min="1" v-model.number="form.duration_days" placeholder="Duration (days)" required />
            <div class="invalid-feedback">Duration must be at least 1 day.</div>
          </div>
          <div class="mb-2">
            <input class="form-control" type="number" min="0" step="0.01" v-model.number="form.price" placeholder="Price" required />
            <div class="invalid-feedback">Price cannot be negative.</div>
          </div>
          <div class="mb-2">
            <input class="form-control" type="number" min="0" v-model.number="form.slots" placeholder="Slots" required />
            <div class="invalid-feedback">Slots cannot be negative.</div>
          </div>
          <p v-if="error" class="text-danger">{{ error }}</p>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button type="submit" class="btn btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
