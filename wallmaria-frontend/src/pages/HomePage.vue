<template>
    <div class="flex flex-col h-full justify-center items-center gap-5">
        <img src="../assets/logo.png" alt="WallMaria logo placeholder" class="w-48 h-42">
    
        <!-- Search bar component -->
        <SearchBar />
    
        <!-- Action buttons component -->
        <ActionButtons />
    
        <!-- Offered language -->
        <p class="text-xs">WallMaria offered in: <a href="#" class="text-blue-600 hover:underline">{{ language }}</a></p>
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import SearchBar from '../components/SearchBar.vue';
import ActionButtons from '../components/ActionButtons.vue';

const language = ref('日本語');
</script>
  
<style scoped>
</style>
  