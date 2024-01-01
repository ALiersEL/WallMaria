<template>
    <div v-if="isOpen" class="w-full fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center overflow-auto py-8 z-50"
        @click="close">
        <div class="modal-container w-1/3 bg-white rounded-lg p-5 shadow-xl relative" @click.stop>
            <!-- Set a specific width -->
            <div class="flex justify-between items-center pb-3">
                <p class="text-2xl font-bold text-center flex-grow">Search any image with WallMaria</p>
                <div class="cursor-pointer z-50" @click="close">
                    <i class="fas fa-times"></i>
                </div>
            </div>
            
            <div class="border-dashed border-2 border-gray-200 rounded flex justify-center items-center p-10 relative"
                @dragover.prevent @dragenter.prevent="dragEnter" @dragleave.prevent="dragLeave"
                @drop.prevent="handleDrop($event)" :class="{ 'bg-blue-100': isDragOver }">
                <!-- Remove Image Button -->
                <button v-if="uploadedImageBase64"
                    class="absolute top-0 right-1 bg-transparent text-gray-500 hover:text-gray-700 font-bold p-1 rounded"
                    @click="removeImage">
                    <i class="fas fa-times"></i>
                </button>

                <!-- Image or Upload Prompt -->
                <img v-if="uploadedImageBase64" :src="uploadedImageBase64" alt="Uploaded image" class="max-w-full h-auto">
                <div v-else class="flex flex-col items-center">
                    <p class="text-gray-500">Drag an image here or <span class="text-blue-600 cursor-pointer"
                            @click="triggerFileUpload">upload a file</span></p>
                    <input type="file" class="hidden" ref="fileInput" @change="handleFileUpload($event)">
                </div>
            </div>
            <div class="pt-3 flex justify-between">
                <input type="text" v-model="imageLink" placeholder="Paste image link"
                    class="border-2 border-gray-200 rounded p-2 w-full">
                <button class="ml-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    @click="search">Search</button>
            </div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const isOpen = ref(false);
const isDragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const uploadedImageBase64 = ref<string | null>(null);
const imageLink = ref<string | null>(null);
const imageToken = ref<string | null>(null);
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
        localStorage.setItem('imageToken', data.token);
        imageToken.value = data.token;
        console.log(data)
        return data.token; // Return the token
    } catch (error) {
        console.error('Error uploading image:', error);
        throw error; // Propagate the error
    }
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

const removeImage = () => {
    if (fileInput.value) {
        fileInput.value.value = ''; // Clear the value of the file input to allow the same file to be selected again
    }
    uploadedImageBase64.value = null;
    imageToken.value = null;
};

const downloadImageAndGetToken = async (imageUrl: string) => {
    try {
        const response = await fetch(imageUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const blob = await response.blob();
        return await getImageToken(blob); // Return the token from getImageToken
    } catch (error) {
        console.error('Error downloading or storing image:', error);
        throw error; // Propagate the error
    }
}

const search = async () => {
    console.log(imageLink.value);
    try {
        console.log(imageToken.value)
        if (imageToken.value) {
            const queryParams: Record<string, string> = {};
            queryParams['token'] = imageToken.value!;
            router.push({ name: 'SearchResults', query: queryParams });
            close();
            return;
        } else if (imageLink.value) {
            const token = await downloadImageAndGetToken(imageLink.value); // Wait for the token
            console.log(token);
            if (token) {
                const queryParams: Record<string, string> = {};
                queryParams['token'] = token;
                router.push({ name: 'SearchResults', query: queryParams });
                close();
            } else {
                alert('Failed to retrieve image token.');
            }
        } else {
            alert('Please upload an image or provide an image URL first.');
        }
    } catch (error) {
        console.error('Error in search process:', error);
        alert('An error occurred during the search process.');
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