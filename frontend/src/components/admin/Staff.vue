<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const staff = ref([]);
const q = ref("");
const showModal = ref(false);
const error = ref("");
const validated = ref(false);
const form = ref({ name: "", email: "", password: "" });

async function load() {
  staff.value = await apiFetch(`/api/admin/staff${q.value ? `?q=${encodeURIComponent(q.value)}` : ""}`);
}
onMounted(load);

function openCreate() {
  form.value = { name: "", email: "", password: "" };
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
    await apiFetch("/api/admin/staff", { method: "POST", body: JSON.stringify(form.value) });
    showModal.value = false;
    await load();
  } catch (e) {
    error.value = e.message;
  }
}

async function toggle(member) {
  await apiFetch(`/api/admin/users/${member.id}/toggle-active`, { method: "PATCH" });
  await load();
}
</script>

<template>
  <div class="d-flex justify-content-between mb-3">
    <input v-model="q" @keyup.enter="load" class="form-control w-auto" placeholder="Search by name/email" />
    <button class="btn btn-primary" @click="openCreate">+ New Staff</button>
  </div>

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
        <tr v-for="s in staff" :key="s.id">
          <td class="fw-medium">{{ s.name }}</td>
          <td>{{ s.email }}</td>
          <td>
            <span :class="s.is_active ? 'badge bg-success' : 'badge bg-danger'">
              {{ s.is_active ? "Active" : "Blacklisted" }}
            </span>
          </td>
          <td>
            <button class="btn btn-sm" :class="s.is_active ? 'btn-danger' : 'btn-success'" @click="toggle(s)">
              {{ s.is_active ? "Blacklist" : "Reinstate" }}
            </button>
          </td>
        </tr>
        <tr v-if="!staff.length">
          <td colspan="4" class="text-center text-muted py-4">No staff yet.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">New Staff</h5>
          <button type="button" class="btn-close" @click="showModal = false"></button>
        </div>
        <form class="modal-body" novalidate :class="{ 'was-validated': validated }" @submit.prevent="onSubmit">
          <div class="mb-2">
            <input class="form-control" v-model="form.name" placeholder="Name" required />
            <div class="invalid-feedback">Name is required.</div>
          </div>
          <div class="mb-2">
            <input class="form-control" type="email" v-model="form.email" placeholder="Email" required />
            <div class="invalid-feedback">Enter a valid email.</div>
          </div>
          <div class="mb-2">
            <input class="form-control" type="password" v-model="form.password" placeholder="Password" minlength="6" required />
            <div class="invalid-feedback">Password must be at least 6 characters.</div>
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
