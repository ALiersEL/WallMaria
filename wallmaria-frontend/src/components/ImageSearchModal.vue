<template>
    <div v-if="isOpen" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center overflow-auto py-8" @click="close">
        <div class="modal-container bg-white rounded-lg p-5 shadow-xl relative" style="width: 600px;" @click.stop> <!-- Set a specific width -->
            <div class="flex justify-between items-center pb-3">
                <p class="text-2xl font-bold text-center flex-grow">Search any image with WallMaria</p>
                <div class="cursor-pointer z-50" @click="close">
                    <i class="fas fa-times"></i>
                </div>
            </div>
            <div 
                class="border-dashed border-2 border-gray-200 rounded flex justify-center items-center p-10 relative"
                @dragover.prevent
                @dragenter.prevent="dragEnter"
                @dragleave.prevent="dragLeave"
                @drop.prevent="handleDrop($event)"
                :class="{ 'bg-blue-100': isDragOver }"
            >   
                <!-- Remove Image Button -->
                <button v-if="uploadedImageBase64" class="absolute top-0 right-1 bg-transparent text-gray-500 hover:text-gray-700 font-bold p-1 rounded" @click="removeImage">
                    <i class="fas fa-times"></i>
                </button>

                <!-- Image or Upload Prompt -->
                <img v-if="uploadedImageBase64" :src="uploadedImageBase64" alt="Uploaded image" class="max-w-full h-auto">
                <div v-else class="flex flex-col items-center">
                    <p class="text-gray-500">Drag an image here or <span class="text-blue-600 cursor-pointer" @click="triggerFileUpload">upload a file</span></p>
                    <input type="file" class="hidden" ref="fileInput" @change="handleFileUpload($event)">
                </div>
            </div>
            <div class="pt-3 flex justify-between">
                <input type="text" v-model="imageLink" placeholder="Paste image link" class="border-2 border-gray-200 rounded p-2 w-full">
                <button class="ml-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="search">Search</button>
            </div>
        </div>
      </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { v4 as uuidv4 } from 'uuid';

const isOpen = ref(false);
const isDragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const uploadedImageBase64 = ref<string | null>(null);
const imageId = ref<string | null>(null);
const imageLink = ref<string | null>(null);
const router = useRouter();

const close = () => {
    isOpen.value = false;
};


const dragEnter = () => {
    isDragOver.value = true;
};

const dragLeave = () => {
    isDragOver.value = false;
};

const displayImage = (file: File) => {
    imageId.value = uuidv4();
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImageBase64.value = e.target?.result as string;
        localStorage.setItem(imageId.value!, uploadedImageBase64.value as string);
    };
    reader.readAsDataURL(file);
};

const handleDrop = (event: DragEvent) => {
    isDragOver.value = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        const files = event.dataTransfer.files;
        const file = files[0];
        displayImage(file);
        // You might want to close the modal or reset the state here
    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const handleFileUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    displayImage(file);
    // Remember to clear the input after the file is handled
    input.value = '';
};

const removeImage = () => {
    if (fileInput.value) {
        fileInput.value.value = ''; // Clear the value of the file input to allow the same file to be selected again
    }
    if (imageId.value) {
        localStorage.removeItem(imageId.value);
    }
    uploadedImageBase64.value = null;
    imageId.value = null;
    imageLink.value = null;
};

const search = () => {
    if (imageId.value || imageLink.value) {
        const queryParams : Record<string, string> = {};
        if (imageId.value) {
            queryParams['image_id'] = imageId.value;
        } else if (imageLink.value) {
            queryParams['image_url'] = imageLink.value;
        }
        router.push({ name: 'ImageSearchResults', query: queryParams });
    } else {
        // Handle case where there is no image or URL provided
        alert('Please upload an image or provide an image URL first.');
    }
};

// Expose the isOpen ref so it can be controlled by the parent component
defineExpose({ isOpen });
</script>
  
<style scoped>
.modal-container {
  margin-top: auto;
  margin-bottom: auto;
}
</style>