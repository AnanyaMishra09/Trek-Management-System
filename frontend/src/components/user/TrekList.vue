<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const treks = ref([]);
const difficulty = ref("");
const location = ref("");
const duration = ref("");
const message = ref("");
const messageType = ref("success");

async function load() {
  const params = new URLSearchParams();
  if (difficulty.value) params.set("difficulty", difficulty.value);
  if (location.value) params.set("location", location.value);
  if (duration.value) params.set("duration", duration.value);
  treks.value = await apiFetch(`/api/user/treks?${params}`);
}
onMounted(load);

async function book(trek) {
  message.value = "";
  try {
    await apiFetch(`/api/user/treks/${trek.id}/book`, { method: "POST" });
    message.value = `Booked "${trek.name}"! Check My History for details.`;
    messageType.value = "success";
    await load();
  } catch (e) {
    message.value = e.message;
    messageType.value = "danger";
  }
}

const bannerClass = (d) => ({ Easy: "easy", Moderate: "moderate", Hard: "hard" }[d] || "easy");
</script>

<template>
  <div class="card p-3 mb-4">
    <div class="d-flex flex-wrap gap-2 align-items-center">
      <select class="form-select w-auto" v-model="difficulty" @change="load">
        <option value="">All difficulties</option>
        <option>Easy</option>
        <option>Moderate</option>
        <option>Hard</option>
      </select>
      <input class="form-control w-auto" v-model="location" @keyup.enter="load" placeholder="Location" />
      <input
        class="form-control w-auto"
        type="number"
        v-model="duration"
        @keyup.enter="load"
        placeholder="Duration (days)"
      />
      <button class="btn btn-primary" @click="load">Search</button>
    </div>
  </div>

  <div v-if="message" class="alert" :class="`alert-${messageType}`">{{ message }}</div>

  <div class="row g-4">
    <div class="col-md-4" v-for="t in treks" :key="t.id">
      <div class="card trek-card h-100">
        <div class="trek-banner" :class="bannerClass(t.difficulty)">⛰</div>
        <div class="card-body d-flex flex-column">
          <div class="d-flex justify-content-between align-items-start mb-1">
            <h5 class="card-title mb-0">{{ t.name }}</h5>
            <span class="badge" :class="`badge-${bannerClass(t.difficulty)}`">{{ t.difficulty }}</span>
          </div>
          <p class="text-muted small mb-2">{{ t.location }} · {{ t.duration_days }} days</p>
          <p class="fs-5 fw-semibold mb-2">₹{{ t.price }}</p>
          <p class="small mb-3">
            <span :class="t.slots > 0 ? 'text-success' : 'text-danger'">
              {{ t.slots > 0 ? `${t.slots} slots left` : "Sold out" }}
            </span>
          </p>
          <button class="btn btn-primary mt-auto" :disabled="t.slots <= 0" @click="book(t)">
            {{ t.slots > 0 ? "Book Now" : "Sold out" }}
          </button>
        </div>
      </div>
    </div>
    <div class="col-12" v-if="!treks.length">
      <div class="text-center text-muted py-5">No treks match your filters. Try widening your search.</div>
    </div>
  </div>
</template>
