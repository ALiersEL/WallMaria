<template>
    <div class="w-full h-full flex flex-col">
        <!-- Header -->
        <header class="bg-white py-4 px-6 flex items-center justify-between shadow h-16">
            <h1 class="text-xl font-bold cursor-pointer" @click="navigateToHome">WallMaria</h1>
            <button class="bg-blue-500 text-white px-4 py-2 rounded ml-4">
                Upload
            </button>
        </header>

        <!-- Main Content -->
        <div class="flex flex-grow overflow-auto">
            <!-- Input Image Display -->
            <div class="bg-stone-800 w-1/2 p-24 flex items-center justify-center">
                <img :src="inputImagePath" alt="Input" class="max-w-full max-h-full w-auto h-auto rounded" />
            </div>

            <!-- Search Results with Masonry Layout -->
            <div class="w-1/2 p-4 flex items-start overflow-auto max-h-[calc(100vh-64px)]" ref="masonryColumns">
                <div class="w-1/3 pr-2" v-for="column in columns" :key="column.id" ref="column">
                    <div v-for="image in column.images" :key="image.id" class="mb-4">
                        <img :src="image.src" :alt="image.alt" class="h-auto rounded mb-2" />
                        <div class="text-sm">
                            <h3 class="max-w-full break-words">{{ image.title }}</h3>
                            <p class="max-w-full break-words">{{ image.source }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import defaultImage from "../assets/download.png";

const route = useRoute();
const router = useRouter();
const inputImagePath = ref<string>(defaultImage);
const columns = ref<any[]>([
    { id: 1, images: [] },
    { id: 2, images: [] },
    { id: 3, images: [] },
]);
const masonryColumns = ref<HTMLElement | null>(null);
interface Image {
    id: number;
    title: string;
    alt: string;
    src: string;
    source: string;
}

// Watch for changes to the route params and update the image path accordingly
watch(
    () => route.query,
    (queryParams) => {
        if (queryParams.image_id) {
            const imageId = queryParams.image_id as string;
            console.log(localStorage.getItem(imageId));
            inputImagePath.value = localStorage.getItem(imageId) || defaultImage;
        } else {
            inputImagePath.value = queryParams.image_url as string;
        }
    },
    { immediate: true }
);

const getColumnHeights = () => {
    return masonryColumns.value
      ? Array.from(masonryColumns.value.children).map(
          (column) => column.clientHeight
      )
      : [];
};

const addImageToShortestColumn = (newImage: Image) => {
    nextTick().then(() => {
        const columnHeights = getColumnHeights();
        console.log(columnHeights);
        const shortestColumnIndex = columnHeights.indexOf(
            Math.min(...columnHeights)
        );
        columns.value[shortestColumnIndex].images.push(newImage);
    });
};

const navigateToHome = () => {
    router.push("/");
};

fetch("api/posts?limit=10")
    .then((response) => response.json())
    .then((data) => {
        const formattedData = data.map((item: any) => ({
            id: item.id,
            title: item.uploader_id,
            alt: item.uploader_id,
            src: item.large_file_url,
            source: item.source,
        }));
        // 每隔 100ms 添加一张图片
        formattedData.forEach((image: Image, index: number) => {
            setTimeout(() => {
                addImageToShortestColumn(image);
            }, index * 10);
        });
    })
    .catch((error) => {
        console.error("Error fetching images:", error);
    });
</script>

<style scoped>
/* Custom styles for masonry layout */
@media (max-width: 768px) {
  .masonry {
    column-count: 2;
  }
}

@media (max-width: 640px) {
  .masonry {
    column-count: 1;
  }
}

.break-inside-avoid {
  break-inside: avoid;
  page-break-inside: avoid;
}
</style>