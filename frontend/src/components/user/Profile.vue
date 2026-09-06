<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const name = ref("");
const email = ref("");
const password = ref("");
const message = ref("");

onMounted(async () => {
  const profile = await apiFetch("/api/user/profile");
  name.value = profile.name;
  email.value = profile.email;
});

async function save() {
  message.value = "";
  const body = { name: name.value };
  if (password.value) body.password = password.value;
  await apiFetch("/api/user/profile", { method: "PUT", body: JSON.stringify(body) });
  password.value = "";
  message.value = "Profile updated.";
}
</script>

<template>
  <div class="card p-4" style="max-width: 28rem">
    <h1 class="h5 mb-3">My Profile</h1>
    <form @submit.prevent="save">
      <div class="mb-3">
        <label class="form-label small text-muted">Email</label>
        <input class="form-control" :value="email" disabled />
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">Name</label>
        <input class="form-control" v-model="name" required />
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">New Password (leave blank to keep current)</label>
        <input class="form-control" type="password" v-model="password" minlength="6" />
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
      <p v-if="message" class="mt-2 text-success small">{{ message }}</p>
    </form>
  </div>
</template>
