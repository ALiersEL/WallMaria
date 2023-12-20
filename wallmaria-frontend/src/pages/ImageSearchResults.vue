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
                <img :src="inputImagePath" alt="Input" class="max-w-full max-h-full w-auto h-auto rounded"
                    ref="imageElement" />
                <!-- Overlay Element -->
                <div class="overlay" :style="overlayStyle"></div>
                <!-- Selection Box -->
                <div class="border-4 border-orange-500 absolute cursor-move" :style="selectionStyle" @mousedown="startDrag">
                    <!-- Resize Handles -->
                    <div class="handle top-left" @mousedown.prevent.stop="initResize('top-left', $event)"></div>
                    <div class="handle top-right" @mousedown.prevent.stop="initResize('top-right', $event)"></div>
                    <div class="handle bottom-left" @mousedown.prevent.stop="initResize('bottom-left', $event)"></div>
                    <div class="handle bottom-right" @mousedown.prevent.stop="initResize('bottom-right', $event)"></div>
                </div>
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
import { ref, reactive, watch, nextTick, computed, onMounted } from "vue";
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
            inputImagePath.value = localStorage.getItem(imageId) || defaultImage;
        } else {
            inputImagePath.value = queryParams.image_url as string;
        }
    },
    { immediate: true }
);

const imageElement = ref<HTMLImageElement | null>(null);
const selectionBox = reactive({
    left: 0,
    top: 0,
    width: 100,
    height: 100,
    resizing: false,
    resizeCorner: '',
});
const dragging = ref(false);
let dragStartX = 0;
let dragStartY = 0;

const startDrag = (event: MouseEvent) => {
    dragging.value = true;
    dragStartX = event.pageX - selectionBox.left;
    dragStartY = event.pageY - selectionBox.top;
    window.addEventListener('mousemove', onDrag);
    window.addEventListener('mouseup', endDrag);
};

const onDrag = (event: MouseEvent) => {
    if (dragging.value && !selectionBox.resizing) {
        selectionBox.left = Math.max(event.pageX - dragStartX, imageElement.value?.offsetLeft!);
        selectionBox.top = Math.max(event.pageY - dragStartY, imageElement.value?.offsetTop!);
        selectionBox.left = Math.min(selectionBox.left, imageElement.value?.offsetLeft! + imageElement.value?.offsetWidth! - selectionBox.width);
        selectionBox.top = Math.min(selectionBox.top, imageElement.value?.offsetTop! + imageElement.value?.offsetHeight! - selectionBox.height);
    }
};

const endDrag = () => {
    dragging.value = false;
    window.removeEventListener('mousemove', onDrag);
    window.removeEventListener('mouseup', endDrag);
};

const initResize = (corner: string, event: MouseEvent) => {
    event.stopPropagation();
    selectionBox.resizing = true;
    selectionBox.resizeCorner = corner;
    window.addEventListener('mousemove', onResize);
    window.addEventListener('mouseup', endResize);
};

const onResize = (event: MouseEvent) => {
    let newWidth: number = selectionBox.width;
    let newHeight: number = selectionBox.height;
    let newLeft: number = selectionBox.left;
    let newTop: number = selectionBox.top;

    switch (selectionBox.resizeCorner) {
        case 'top-left':
            newWidth = Math.max(selectionBox.width + selectionBox.left - event.pageX, 100);
            newHeight = Math.max(selectionBox.height + selectionBox.top - event.pageY, 100);
            newLeft = Math.min(event.pageX, selectionBox.left + selectionBox.width - 100);
            newTop = Math.min(event.pageY, selectionBox.top + selectionBox.height - 100);
            break;
        case 'top-right':
            newWidth = Math.max(event.pageX - selectionBox.left, 100);
            newHeight = Math.max(selectionBox.height + selectionBox.top - event.pageY, 100);
            newTop = Math.min(event.pageY, selectionBox.top + selectionBox.height - 100);
            break;
        case 'bottom-left':
            newWidth = Math.max(selectionBox.width + selectionBox.left - event.pageX, 100);
            newHeight = Math.max(event.pageY - selectionBox.top, 100);
            newLeft = Math.min(event.pageX, selectionBox.left + selectionBox.width - 100);
            break;
        case 'bottom-right':
            newWidth = Math.max(event.pageX - selectionBox.left, 100);
            newHeight = Math.max(event.pageY - selectionBox.top, 100);
            break;
    }

    if (imageElement.value) {
        selectionBox.left = Math.max(newLeft, imageElement.value.offsetLeft);
        selectionBox.top = Math.max(newTop, imageElement.value.offsetTop);
        selectionBox.width = Math.min(newWidth, imageElement.value.offsetWidth - (selectionBox.left - imageElement.value.offsetLeft));
        selectionBox.height = Math.min(newHeight, imageElement.value.offsetHeight - (selectionBox.top - imageElement.value.offsetTop));
    }
};

const endResize = () => {
    selectionBox.resizing = false;
    window.removeEventListener('mousemove', onResize);
    window.removeEventListener('mouseup', endResize);
};

// Add a computed property to bind the selection box style
const selectionStyle = computed(() => ({
    left: `${selectionBox.left}px`,
    top: `${selectionBox.top}px`,
    width: `${selectionBox.width}px`,
    height: `${selectionBox.height}px`,
}));

onMounted(() => {
    // 等待图片加载完成后，设置选择框的初始位置
    imageElement.value?.addEventListener('load', () => {
        selectionBox.left = imageElement.value?.offsetLeft! + imageElement.value?.offsetWidth! / 4;
        selectionBox.top = imageElement.value?.offsetTop! + imageElement.value?.offsetHeight! / 4;
        selectionBox.width = imageElement.value?.offsetWidth! / 2;
        selectionBox.height = imageElement.value?.offsetHeight! / 2;
    });
});

// // Add a computed property for the overlay style
const overlayStyle = computed(() => {
    if (!imageElement.value) return {};

    const overlayLeft = `${imageElement.value.offsetLeft}px`;
    const overlayTop = `${imageElement.value.offsetTop}px`;
    const overlayWidth = `${imageElement.value.offsetWidth}px`;
    const overlayHeight = `${imageElement.value.offsetHeight}px`;

    const outerTopLeft = `0px 0px`;
    const outerTopRight = `${imageElement.value.offsetWidth}px 0px`;
    const outerBottomRight = `${imageElement.value.offsetWidth}px ${imageElement.value.offsetHeight}px`;
    const outerBottomLeft = `0px ${imageElement.value.offsetHeight}px`;

    // 内部长方形 (selectionBox)
    const innerTopLeft = `${selectionBox.left - imageElement.value.offsetLeft}px ${selectionBox.top - imageElement.value.offsetTop}px`;
    const innerTopRight = `${selectionBox.left - imageElement.value.offsetLeft + selectionBox.width}px ${selectionBox.top - imageElement.value.offsetTop}px`;
    const innerBottomRight = `${selectionBox.left - imageElement.value.offsetLeft + selectionBox.width}px ${selectionBox.top - imageElement.value.offsetTop + selectionBox.height}px`;
    const innerBottomLeft = `${selectionBox.left - imageElement.value.offsetLeft}px ${selectionBox.top - imageElement.value.offsetTop + selectionBox.height}px`;

    const intersectionBottomLeft = `${selectionBox.left - imageElement.value.offsetLeft}px ${imageElement.value.offsetHeight}px`;

    return {
        left: overlayLeft,
        top: overlayTop,
        width: overlayWidth,
        height: overlayHeight,
        clipPath: `polygon(${outerTopLeft}, ${outerBottomLeft}, ${intersectionBottomLeft}, ${innerTopLeft}, ${innerTopRight}, ${innerBottomRight}, ${innerBottomLeft}, ${intersectionBottomLeft}, ${outerBottomRight}, ${outerTopRight})`
    };
});

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
.overlay {
  position: absolute;
  background-color: rgba(58, 53, 53, 0.5);
  pointer-events: none;
}

.handle {
  width: 20px;
  height: 20px;
  position: absolute;
}

.handle.top-left {
  top: -5px;
  left: -5px;
  cursor: nwse-resize;
}

.handle.top-right {
  top: -5px;
  right: -5px;
  cursor: nesw-resize;
}

.handle.bottom-left {
  bottom: -5px;
  left: -5px;
  cursor: nesw-resize;
}

.handle.bottom-right {
  bottom: -5px;
  right: -5px;
  cursor: nwse-resize;
}

img {
  /* 火狐 */
  -moz-user-select: none;
  /* Safari 和 欧朋 */
  -webkit-user-select: none;
  /* IE10+ and Edge */
  -ms-user-select: none;
  /* Standard syntax 标准语法(谷歌) */
  user-select: none;
}

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