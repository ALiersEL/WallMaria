<template>
    <div class="flex items-start justify-start space-x-4">
        <!-- 头像 -->
        <a :href="profile.source == '' ? profile.avatarUrl : profile.source" target="_blank" rel="noopener noreferrer">
            <img class="w-12 h-12 rounded-full" :src="profile.avatarUrl" alt="Profile avatar" />
        </a>
        <!-- 名字和百分比 -->
        <div class="flex flex-col">
            <span class="font-semibold w-32 truncate ...">{{ profile.name }}</span>
            <span class="text-gray-600">{{ profile.percentage }}%</span>
        </div>
    </div>
</template>
  
<script setup lang="ts">
interface ProfileBlockProps {
    name: string;
    avatarUrl: string;
    percentage: number;
    source: string;
}

const profile: ProfileBlockProps = defineProps({
    name: {
        type: String,
        required: true
    },
    avatarUrl: {
        type: String,
        required: true
    },
    percentage: {
        type: Number,
        required: true
    },
    source: {
        type: String,
        required: true
    }
});
</script>
  
<style>
/* 可以添加一些额外的 CSS 样式，如果需要的话 */
</style>
  