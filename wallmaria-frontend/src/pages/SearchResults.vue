<template>
    <div class="w-full h-full flex flex-col">
        <!-- Header -->
        <header class="bg-white py-4 px-6 flex items-center justify-between shadow h-16">
            <div>
                <h1 class="text-xl font-bold cursor-pointer" @click="navigateToHome">WallMaria</h1>
            </div>
            <div class="flex-1 flex justify-end">
                <input type="text" class="border rounded-full w-1/2 h-10 pl-5 pr-10 text-sm focus:outline-none"
                    v-model="searchQuery" @keyup.enter="onInputEnter" placeholder="Search WallMaria or type a URL"
                    style="max-width: calc(50% - 90px);" />
                <button class="bg-blue-500 text-white px-4 py-2 rounded ml-4" @click="openImageSearchModal">
                    Upload
                </button>
                <ImageSearchModal ref="imageSearchModal" />
            </div>
        </header>

        <!-- Main Content -->
        <div class="flex flex-grow overflow-auto">
            <!-- Input Image Display -->
            <div v-if="inputImagePath === null" class="w-1/2 h-full flex justify-center items-center ">
                <ImageUpload class="w-2/3 h-4/5" />
            </div>
            <div v-else class="bg-stone-800 w-1/2 p-24 flex items-center justify-center">
                <img :src="inputImagePath!" alt="Input" class="max-w-full max-h-full w-auto h-auto rounded"
                    ref="imageElement" />
                <!-- Overlay Element -->
                <div class="overlay" :style="overlayStyle"></div>
                <!-- Selection Box -->
                <div v-if="imageLoaded" class="border-4 border-orange-500 absolute cursor-move" :style="selectionStyle"
                    @mousedown="startDrag">
                    <!-- Resize Handles -->
                    <div class="handle top-left" @mousedown.prevent.stop="initResize('top-left', $event)"></div>
                    <div class="handle top-right" @mousedown.prevent.stop="initResize('top-right', $event)"></div>
                    <div class="handle bottom-left" @mousedown.prevent.stop="initResize('bottom-left', $event)"></div>
                    <div class="handle bottom-right" @mousedown.prevent.stop="initResize('bottom-right', $event)"></div>
                </div>
            </div>


            <div class="w-1/2 container mx-auto overflow-auto max-h-[calc(100vh-64px)]">
                <div class="grid grid-cols-4 gap-4 ml-6 mt-4">
                    <ProfileBlock v-for="info in predictionInfo" :key="info.name" :name="info.name"
                        :avatarUrl="info.previewUrl" :percentage="info.occurrences * 10" :source="info.source" />
                </div>

                <!-- Search Results with Masonry Layout -->
                <div class="w-full p-4 flex items-start" ref="masonryColumns">
                    <div class="w-1/3 pr-2" v-for="(column, index) in columns" :key="column.id" ref="column">
                        <div v-for="image in column.images" :key="image.id" class="mb-4">
                            <a :href="image.source" target="_blank" class="block">
                                <img :src="image.src" :alt="image.alt" class="h-auto rounded-lg mb-2" />
                            </a>
                            <div class="text-sm" ref="imageInfo">
                                <p class="max-w-full break-words line-clamp-3">{{ image.tagStringCharacter }}</p>
                            </div>
                        </div>
                        <div :ref="(setSentinelRef(index) as VNodeRef)"></div> <!-- 哨兵元素 -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, Ref, reactive, watch, nextTick, computed, onMounted, VNodeRef } from "vue";
import { useRoute, useRouter } from "vue-router";
import BigNumber from "bignumber.js";
import ImageUpload from "../components/ImageUpload.vue";
import ImageSearchModal from "../components/ImageSearchModal.vue";
import ProfileBlock from "../components/ProfileBlock.vue";

const route = useRoute();
const router = useRouter();
const inputImagePath = ref<string | null>(null);
const columns = ref<any[]>([
    { id: 1, images: [] },
    { id: 2, images: [] },
    { id: 3, images: [] },
]);
const masonryColumns = ref<HTMLElement | null>(null);
const columnHeights = ref<BigNumber[]>([new BigNumber('0'), new BigNumber('0'), new BigNumber('0')]);
const columnNumber = ref<number>(3);
interface Image {
    id: number;
    title: string;
    alt: string;
    src: string;
    source: string;
    width: number;
    height: number;
    tagStringCharacter: string;
}

const imageToken = ref<string | null>(null);
const searchQuery = ref<string | null>(null);
let page: number = 1;
let imageLoaded: boolean = false;
let rank: number = 0;
let isRequestPending: boolean = false;
interface PredictionInfo {
    type: string;
    name: string;
    previewUrl: string;
    source: string;
    occurrences: number;
}
let predictionInfo: PredictionInfo[] = [];

const clearImages = () => {
    // 清空
    columns.value.forEach((column) => {
        column.images = [];
    });
    page = 1;
    rank = 0;
    columnHeights.value = [new BigNumber('0'), new BigNumber('0'), new BigNumber('0')];
};


// Watch for changes to the route params and update the image path accordingly
watch(
    () => route.query,
    (queryParams) => {
        if (queryParams.token && queryParams.q) {
            imageToken.value = queryParams.token as string;
            searchQuery.value = queryParams.q as string;
            inputImagePath.value = `/api/searches/${imageToken.value}`;
        }
        else if (queryParams.token) {
            imageToken.value = queryParams.token as string;
            searchQuery.value = null;
            inputImagePath.value = `/api/searches/${imageToken.value}`;
        }
        else if (queryParams.q) {
            imageToken.value = null;
            searchQuery.value = queryParams.q as string;
            inputImagePath.value = null;
        }
        clearImages();
    },
    { immediate: true }
);

// Watch Input Image Path from null to not null
watch(
    inputImagePath,
    (newInputImagePath, oldInputImagePath) => {
        // console.log("watch inputImagePath", newInputImagePath, oldInputImagePath);
        if (newInputImagePath && !oldInputImagePath) {
            nextTick().then(() => {
                imageElement.value?.addEventListener('load', () => {
                    // console.log("imageElement.value?.addEventListener('load'");
                    selectionBox.left = imageElement.value?.offsetLeft!;
                    selectionBox.top = imageElement.value?.offsetTop!;
                    selectionBox.width = imageElement.value?.offsetWidth!;
                    selectionBox.height = imageElement.value?.offsetHeight!;
                    imageLoaded = true;
                    loadMoreImages();
                });
            });
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

const getNaturalCropBox = () => {
    const scaleX = imageElement.value!.naturalWidth / imageElement.value!.width;
    const scaleY = imageElement.value!.naturalHeight / imageElement.value!.height;

    return {
        left: Math.floor((selectionBox.left - imageElement.value!.offsetLeft) * scaleX),
        top: Math.floor((selectionBox.top - imageElement.value!.offsetTop) * scaleY),
        width: Math.floor(selectionBox.width * scaleX),
        height: Math.floor(selectionBox.height * scaleY),
    };
};

const loadMoreImages = async () => {
    if (!imageToken.value && !searchQuery.value) return;
    if (page == 1 && imageToken.value) {
        fetchPrediction();
    }

    if (imageToken.value && searchQuery.value) {
        fetchImagesByImageTokenAndSearchQuery();
    }
    else if (imageToken.value) {
        fetchImagesByImageToken();
    }
    else if (searchQuery.value) {
        fetchImagesBySearchQuery();
    }
};

const fetchPrediction = async () => {
    if (!imageToken.value) return;
    // if(isRequestPending) return;
    const cropBox = getNaturalCropBox();
    if (cropBox.width === 0 || cropBox.height === 0 || isNaN(cropBox.width) || isNaN(cropBox.height)) return;

    // isRequestPending = true;
    const params = new URLSearchParams({
        token: imageToken.value,
        left: cropBox.left.toString(),
        top: cropBox.top.toString(),
        width: cropBox.width.toString(),
        height: cropBox.height.toString(),
    });

    // console.log("fetchPrediction", params.toString());

    fetch('api/predict_image_info?' + params.toString())
        .then((response) => response.json())
        .then((data) => {
            predictionInfo = data.map((item: any) => ({
                type: item.type,
                name: item.name,
                previewUrl: item.preview_url,
                source: item.source,
                occurrences: item.occurrences,
            }));
            // isRequestPending = false;
        })
        .catch((error) => {
            console.error("Error fetching images:", error);
            // isRequestPending = false;
        });
};

const selectBestImageUrl = (data: any) => {
    const isOriginalInPath = (url: string) => /\/original\//.test(url);

    if (!isOriginalInPath(data.file_url)) {
        return data.file_url;
    } else if (!isOriginalInPath(data.large_file_url)) {
        return data.large_file_url;
    } else {
        let nonOriginalVariants = data.media_asset.variants.filter((variant: { type: string; }) => variant.type !== 'original');
        if (nonOriginalVariants.length === 0) {
            return null; // No suitable variant found
        }
        let highestResolutionVariant = nonOriginalVariants.reduce((max: { width: number; height: number; }, variant: { width: number; height: number; }) => 
            (variant.width * variant.height > max.width * max.height) ? variant : max
        );
        return highestResolutionVariant.url;
    }
}


// 接收一个json对象，转化成Image类型
const formatData = (dataArray: any[]) => {
    return dataArray.map(item => ({
        id: item.id,
        title: item.id,
        alt: item.id,
        src: selectBestImageUrl(item),
        source: item.source,
        width: item.image_width,
        height: item.image_height,
        tagStringCharacter: item.tag_string_character.replace(/_/g, " ")
    }));
}

const fetchImagesByImageTokenAndSearchQuery = async () => {
    if (!imageToken.value || !searchQuery.value) return;
    if (isRequestPending) return;
    const cropBox = getNaturalCropBox();
    if (cropBox.width === 0 || cropBox.height === 0 || isNaN(cropBox.width) || isNaN(cropBox.height)) return;

    isRequestPending = true;
    const params = new URLSearchParams({
        token: imageToken.value,
        text: searchQuery.value,
        page: page.toString(),
        left: cropBox.left.toString(),
        top: cropBox.top.toString(),
        width: cropBox.width.toString(),
        height: cropBox.height.toString(),
        alpha: "0.5",
    });

    console.log("loadMoreImages", params.toString());


    fetch('api/search_by_image_text?' + params.toString())
        .then((response) => response.json())
        .then((data) => {
            const formattedData = formatData(data);
            for (const image of formattedData) {
                image.title = image.title + " " + rank;
                rank++;
            }
            console.log(data.map((item: any) => item.id));
            // Add images to the page, adjust the timeout as needed
            formattedData.forEach((image: Image) => {
                addImageToShortestColumn(image);
            });
            page++;
            isRequestPending = false;
        })
        .catch((error) => {
            console.error("Error fetching images:", error);
            isRequestPending = false;
        });
};

const fetchImagesByImageToken = async () => {
    if (!imageToken.value) return;
    if (isRequestPending) return;
    const cropBox = getNaturalCropBox();
    if (cropBox.width === 0 || cropBox.height === 0 || isNaN(cropBox.width) || isNaN(cropBox.height)) return;

    isRequestPending = true;
    const params = new URLSearchParams({
        token: imageToken.value,
        page: page.toString(),
        left: cropBox.left.toString(),
        top: cropBox.top.toString(),
        width: cropBox.width.toString(),
        height: cropBox.height.toString(),
    });

    console.log("loadMoreImages", params.toString());

    fetch('api/search_by_crop?' + params.toString())
        .then((response) => response.json())
        .then((data) => {
            const formattedData = formatData(data);
            for (const image of formattedData) {
                image.title = image.title + " " + rank;
                rank++;
            }
            console.log(data.map((item: any) => item.id));
            // Add images to the page, adjust the timeout as needed
            formattedData.forEach((image: Image) => {
                addImageToShortestColumn(image);
            });
            page++;
            isRequestPending = false;
        })
        .catch((error) => {
            console.error("Error fetching images:", error);
            isRequestPending = false;
        });
};

const fetchImagesBySearchQuery = async () => {
    if (!searchQuery.value) return;
    if (isRequestPending) return;

    isRequestPending = true;

    const params = new URLSearchParams({
        text: searchQuery.value,
        page: page.toString(),
    });

    console.log("loadMoreImages", params.toString());


    fetch('api/search_by_text?' + params.toString())
        .then((response) => response.json())
        .then((data) => {
            const formattedData = formatData(data);
            // Add images to the page, adjust the timeout as needed
            formattedData.forEach((image: Image) => {
                addImageToShortestColumn(image);
            });
            for (const image of formattedData) {
                image.title = image.title + " " + rank;
                rank++;
            }
            page++;
            isRequestPending = false;
        })
        .catch((error) => {
            console.error("Error fetching images:", error);
            isRequestPending = false;
        });

};

const sentinelRefs: Ref<Element>[] = [];
const setSentinelRef = (index: number) => (el: Element) => {
    if (el) {
        sentinelRefs[index] = ref(el);
    }
};

const createObserver = () => {
    sentinelRefs.forEach((sentinelRef) => {
        const observer = new IntersectionObserver((entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    loadMoreImages();
                    break;
                }
            }
        });
        if (sentinelRef.value) {
            observer.observe(sentinelRef.value);
        }
    });
};

const onInputEnter = () => {
    if (searchQuery.value) {
        let params: any = {
            q: searchQuery.value,
        };
        if (imageToken.value) {
            params['token'] = imageToken.value;
        }
        router.push({ query: params });
    }
    else if (imageToken.value) {
        let params: any = {
            token: imageToken.value,
        };
        router.push({ query: params });
    }
};

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
    // 清空
    clearImages();
    loadMoreImages();
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
    // 清空
    clearImages();
    loadMoreImages();
};

// Add a computed property to bind the selection box style
const selectionStyle = computed(() => ({
    left: `${selectionBox.left}px`,
    top: `${selectionBox.top}px`,
    width: `${selectionBox.width}px`,
    height: `${selectionBox.height}px`,
}));

onMounted(() => {
    console.log("onMounted");
    createObserver();
});

// // Add a computed property for the overlay style
const overlayStyle = computed(() => {
    if (!imageElement.value) return {};

    const overlayLeft = imageElement.value.offsetLeft - 1
    const overlayTop = imageElement.value.offsetTop - 1
    const overlayWidth = imageElement.value.offsetWidth + 1
    const overlayHeight = imageElement.value.offsetHeight + 1

    const outerTopLeft = `0px 0px`;
    const outerTopRight = `${overlayWidth}px 0px`;
    const outerBottomRight = `${overlayWidth}px ${overlayHeight}px`;
    const outerBottomLeft = `0px ${overlayHeight}px`;

    // 内部长方形 (selectionBox)
    const innerTopLeft = `${selectionBox.left - overlayLeft}px ${selectionBox.top - overlayTop}px`;
    const innerTopRight = `${selectionBox.left - overlayLeft + selectionBox.width}px ${selectionBox.top - overlayTop}px`;
    const innerBottomRight = `${selectionBox.left - overlayLeft + selectionBox.width}px ${selectionBox.top - overlayTop + selectionBox.height}px`;
    const innerBottomLeft = `${selectionBox.left - overlayLeft}px ${selectionBox.top - overlayTop + selectionBox.height}px`;

    const intersectionBottomLeft = `${selectionBox.left - overlayLeft}px ${overlayHeight}px`;

    return {
        left: `${overlayLeft}px`,
        top: `${overlayTop}px`,
        width: `${overlayWidth}px`,
        height: `${overlayHeight}px`,
        clipPath: `polygon(${outerTopLeft}, ${outerBottomLeft}, ${intersectionBottomLeft}, ${innerTopLeft}, ${innerTopRight}, ${innerBottomRight}, ${innerBottomLeft}, ${intersectionBottomLeft}, ${outerBottomRight}, ${outerTopRight})`
    };
});


const calculateImageDisplayHeight = (imageWidthBigNumber: BigNumber, imageHeightBigNumber: BigNumber, columnWidthBigNumber: BigNumber, marginBottomBigNumber: BigNumber) => {
    return imageHeightBigNumber.multipliedBy(columnWidthBigNumber).dividedBy(imageWidthBigNumber).plus(marginBottomBigNumber);
};

const addImageToShortestColumn = (newImage: Image) => {
    nextTick().then(() => {
        const shortestColumnIndex = columnHeights.value!.reduce((shortestIndex, columnHeight, index) => {
            if (columnHeight.isLessThan(columnHeights.value![shortestIndex])) {
                console.log("shortestIndex", shortestIndex, "columnHeight", columnHeight.toString(), "index", index, "columnHeights.value![shortestIndex]", columnHeights.value![shortestIndex].toString())
                return index;
            } else {
                return shortestIndex;
            }
        }, 0);
        columns.value[shortestColumnIndex].images.push(newImage);
        const imageWidthBigNumber = new BigNumber(newImage.width.toString());
        const imageHeightBigNumber = new BigNumber(newImage.height.toString());
        const columnWidthBigNumber = new BigNumber(masonryColumns.value!.offsetWidth.toString()).dividedBy(new BigNumber(columnNumber.value.toString()));
        const marginBottomBigNumber = new BigNumber('8');
        const columnHeight = calculateImageDisplayHeight(imageWidthBigNumber, imageHeightBigNumber, columnWidthBigNumber, marginBottomBigNumber);
        columnHeights.value[shortestColumnIndex] = columnHeights.value[shortestColumnIndex].plus(columnHeight);
    });
};

const navigateToHome = () => {
    router.push("/");
};

interface ImageSearchModalInterface {
    isOpen: boolean;
}
const imageSearchModal = ref<Ref<ImageSearchModalInterface> | null>(null);

const openImageSearchModal = () => {
    if (imageSearchModal.value) {
        imageSearchModal.value.isOpen = true;
    }
};
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
}</style>