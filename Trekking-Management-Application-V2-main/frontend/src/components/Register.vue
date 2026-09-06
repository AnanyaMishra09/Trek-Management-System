<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const success = ref(false);
const validated = ref(false);
const router = useRouter();

async function onSubmit(e) {
  validated.value = true;
  if (!e.target.checkValidity()) return;
  await submit();
}

async function submit() {
  error.value = "";
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name.value, email: email.value, password: password.value }),
  });
  const data = await res.json();
  if (!res.ok) {
    error.value = data.error || "Registration failed";
    return;
  }
  success.value = true;
  setTimeout(() => router.push("/login"), 1000);
}
</script>

<template>
  <div class="auth-shell d-flex justify-content-center align-items-center vh-100">
    <form
      novalidate
      :class="{ 'was-validated': validated }"
      class="auth-card card p-4 p-md-5 shadow-lg"
      style="width: 24rem"
      @submit.prevent="onSubmit"
    >
      <div class="text-center mb-4">
        <div class="auth-mark">⛰️</div>
        <h1 class="h4 mt-2 mb-0">Join the trek</h1>
        <p class="text-muted small mb-0">Create your trekker account</p>
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">Name</label>
        <input class="form-control" v-model="name" placeholder="Your name" required />
        <div class="invalid-feedback">Name is required.</div>
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">Email</label>
        <input class="form-control" v-model="email" type="email" placeholder="you@example.com" required />
        <div class="invalid-feedback">Enter a valid email.</div>
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">Password</label>
        <input
          class="form-control"
          v-model="password"
          type="password"
          placeholder="At least 6 characters"
          required
          minlength="6"
        />
        <div class="invalid-feedback">Password must be at least 6 characters.</div>
      </div>
      <button class="btn btn-primary w-100" type="submit">Register</button>
      <p v-if="error" class="text-danger mt-2 mb-0 small">{{ error }}</p>
      <p v-if="success" class="text-success mt-2 mb-0 small">Registered! Redirecting to login...</p>
      <router-link class="d-block text-center mt-4 small" to="/login">Already have an account? Login</router-link>
    </form>
  </div>
</template>
