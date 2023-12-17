<template>
  <div class="w-full">
    <!-- Header -->
    <header class="bg-white py-4 px-6 flex items-center justify-between shadow">
      <h1 class="text-xl font-bold">WallMaria</h1>
      <button class="bg-blue-500 text-white px-4 py-2 rounded ml-4">Upload</button>
    </header>

    <!-- Main Content -->
    <div class="flex mt-4">
      <!-- Input Image Display -->
      <div class="w-1/2 p-4">
        <img :src="inputImagePath" alt="Input" class="w-full h-auto rounded">
      </div>

      <!-- Search Results with Masonry Layout -->
      <div class="w-1/2 p-4 flex items-start" ref="masonryColumns">
        <div class="w-1/3 pr-2" v-for="column in columns" :key="column.id" ref="column">
          <div v-for="image in column.images" :key="image.id" class="mb-4">
            <img :src="image.src" :alt="image.alt" class="h-auto rounded mb-2">
            <div class="text-sm">
              <h3>{{ image.title }}</h3>
              <p>{{ image.source }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const inputImagePath = ref<string>('default-image.jpg');
const columns = ref<any[]>([
  { id: 1, images: [] },
  { id: 2, images: [] },
  { id: 3, images: [] }
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
  () => route.params,
  (params) => {
    inputImagePath.value = (params.imagePath || 'default-image.jpg').toString();
  },
  { immediate: true }
);


const getColumnHeights = () => {
  return masonryColumns.value ? Array.from(masonryColumns.value.children).map(column => column.clientHeight) : [];
};

const addImageToShortestColumn = (newImage: Image) => {
  nextTick().then(() => {
    const columnHeights = getColumnHeights();
    console.log(columnHeights);
    const shortestColumnIndex = columnHeights.indexOf(Math.min(...columnHeights));
    columns.value[shortestColumnIndex].images.push(newImage);
  });
};


fetch('api/posts?limit=10')
  .then(response => response.json())
  .then(data => {
    const formattedData = data.map((item: any) => ({
      id: item.id,
      title: item.uploader_id,
      alt: item.uploader_id,
      src: item.large_file_url,
      source: item.source
    }));
    // 每隔 100ms 添加一张图片
    formattedData.forEach((image: Image, index: number) => {
      setTimeout(() => {
        addImageToShortestColumn(image);
      }, index * 10);
    });
  })
  .catch(error => {
    console.error('Error fetching images:', error);
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
  