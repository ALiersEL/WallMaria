<template>
    <div class="modal-container relative"> 
        <div class="border-dashed border-2 border-gray-200 flex justify-center items-center relative h-full" @dragover.prevent
            @dragenter.prevent="dragEnter" @dragleave.prevent="dragLeave" @drop.prevent="handleDrop($event)"
            :class="{ 'bg-blue-100': isDragOver }">

            <!-- Image or Upload Prompt -->
            <img v-if="uploadedImageBase64" :src="uploadedImageBase64" alt="Uploaded image" class="w-full h-full">
            <div v-else class="flex flex-col items-center">
                <p class="text-gray-500">Drag an image here or <span class="text-blue-600 cursor-pointer"
                        @click="triggerFileUpload">upload a file</span></p>
                <input type="file" class="hidden" ref="fileInput" @change="handleFileUpload($event)">
            </div>
        </div>
    </div>
</template>

  
<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const isDragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const uploadedImageBase64 = ref<string | null>(null);
const imageToken = ref<string | null>(null);;
const route = useRoute();
const router = useRouter();

const dragEnter = () => {
    isDragOver.value = true;
};

const dragLeave = () => {
    isDragOver.value = false;
};

const getImageToken = async (image: File | Blob) => {
    const formData = new FormData();
    formData.append('file', image, 'image.png');

    try {
        const response = await fetch('/api/upload_image', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Store the token in local storage
        localStorage.setItem('imageToken', data.token);
        imageToken.value = data.token;
    } catch (error) {
        console.error('Error uploading image:', error);
    }
};

const search = () => {
    if (imageToken.value) {
        const queryParams: Record<string, string> = {};
        if (route.query.q) {
            queryParams['q'] = route.query.q as string;
        }
        queryParams['token'] = imageToken.value!;
        router.push({ name: 'SearchResults', query: queryParams });
    } else {
        // Handle case where there is no image or URL provided
        alert('Please upload an image or provide an image URL first.');
    }
};

const handleDrop = async (event: DragEvent) => {
    isDragOver.value = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        const files = event.dataTransfer.files;
        const file = files[0];
        await getImageToken(file);
        search();
    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const handleFileUpload = async (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    await getImageToken(file);
    search();
    // Remember to clear the input after the file is handled
    input.value = '';
};
</script>
  
<style scoped>
.modal-container {
    margin-top: auto;
    margin-bottom: auto;
}
</style>