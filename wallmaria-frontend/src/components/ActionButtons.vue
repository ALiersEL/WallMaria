<template>
    <div class="flex gap-4 justify-center mt-4">
        <button class="bg-gray-300 hover:bg-gray-200 text-sm py-2 px-4 rounded focus:outline-none" @click="wallMariaSearch">
            WallMaria Search
        </button>
        <button class="bg-gray-300 hover:bg-gray-200 text-sm py-2 px-4 rounded focus:outline-none" @click="feelingLucky">
            I'm Feeling Lucky
        </button>
    </div>
</template>
  
<script setup lang="ts">
const wallMariaSearch = () => {
    // Placeholder for WallMaria Search functionality
    alert('WallMaria Search clicked');
};

const feelingLucky = () => {
    // Placeholder for I'm Feeling Lucky functionality
    alert("I'm Feeling Lucky clicked");
};
</script>
  
<style>
/* Add any specific styles for your action buttons here */
</style>
  