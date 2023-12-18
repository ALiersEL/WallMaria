<template>
    <div class="relative">
        <input type="text" class="border rounded-full w-96 h-10 pl-5 pr-10 text-sm focus:outline-none" v-model="searchQuery"
            @keyup.enter="search" placeholder="Search WallMaria or type a URL" />
        <button
            class="absolute top-2.5 right-3 flex items-center justify-center bg-no-repeat bg-center text-transparent w-5 h-5"
            :style="{ backgroundImage: `url(${imageSearchIcon})`, backgroundSize: 'cover' }" @click="openImageSearchModal"
            title="Search by image">
            <!-- The text for screen readers -->
            <span>Search by image</span>
        </button>

        <!-- Image Search Modal -->
        <ImageSearchModal ref="imageSearchModal" />
    </div>
</template>
  
<script setup lang="ts">
import { ref, Ref } from 'vue';
import imageSearchIcon from '../assets/image-search-icon.png';
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
  