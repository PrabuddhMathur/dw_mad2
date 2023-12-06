<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <body>
    <div id="app">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <router-link to="/" class="navbar-brand">Home</router-link>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            </ul>
          </div>
        </div>
      </nav>
      <router-view />
    </div>
  </body>
</template>

