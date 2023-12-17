<template>
    <div class="relative">
        <input
            type="text"
            class="border rounded-full w-96 h-10 pl-5 pr-10 text-sm focus:outline-none"
            v-model="searchQuery"
            @keyup.enter="search"
            placeholder="Search WallMaria or type a URL"
        />
        <button
            class="absolute top-1 right-3 flex items-center justify-center bg-no-repeat bg-center text-transparent w-8 h-8"
            :style="{ backgroundImage: `url(${imageSearchIcon})` }"
            @click="openImageSearchModal"
            title="Search by image"
            >
            <!-- The text for screen readers -->
            <span>Search by image</span>
        </button>

        <!-- Image Search Modal -->
        <ImageSearchModal ref="imageSearchModal" />
    </div>
</template>
  
<script setup lang="ts">
import { ref, Ref } from 'vue';
import imageSearchIcon from '../assets/image-search-icon.svg';
import ImageSearchModal from './ImageSearchModal.vue';

interface ImageSearchModalInterface {
    isOpen: boolean;
}

const searchQuery = ref('');
const imageSearchModal = ref<Ref<ImageSearchModalInterface> | null>(null);

const search = () => {
    alert(`Searching for: ${searchQuery.value}`);
};

const openImageSearchModal = () => {
  if (imageSearchModal.value) {
      imageSearchModal.value.isOpen = true;
  }
};
</script>
  
<style>
/* Add any specific styles for your search bar here */
</style>
  