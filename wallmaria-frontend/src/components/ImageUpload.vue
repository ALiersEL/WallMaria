<template>
    <div class="modal-container bg-white relative"> <!-- 将模态容器的宽高设置为父 div 的一半 -->
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

<!-- 保留剩余的脚本和样式不变 -->

  
<script setup lang="ts">
import { ref } from 'vue';

const isDragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const uploadedImageBase64 = ref<string | null>(null);
const imageToken = ref<string | null>(null);;

const dragEnter = () => {
    isDragOver.value = true;
};

const dragLeave = () => {
    isDragOver.value = false;
};

const getImageToken = async (image: File | Blob) => {
    const formData = new FormData();
    formData.append('file', image, 'image.png');
    fetch('/api/upload_image', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            // Store the token in local storage
            localStorage.setItem('imageToken', data.token);
            imageToken.value = data.token;
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
};

const displayImage = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImageBase64.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
};

const handleDrop = (event: DragEvent) => {
    isDragOver.value = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        const files = event.dataTransfer.files;
        const file = files[0];
        getImageToken(file);
        displayImage(file);
    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const handleFileUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    getImageToken(file);
    displayImage(file);
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