<template>
  <div>
    <button @click="toggleVideo">{{ watchingVideo ? '退出' : '查看视频' }}</button>
    <div v-if="watchingVideo">
      <img :src="videoUrl" ref="imageRef" alt="Video Stream" />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'VideoComponent',
  data() {
    return {
      watchingVideo: false,
      videoUrl: '', // 后端返回的图片地址
      intervalId: null, // 用于存储定时器ID
    };
  },
  methods: {
    async toggleVideo() {
      if (this.watchingVideo) {
        // 如果正在观看视频，则停止定时请求
        clearInterval(this.intervalId);
        this.watchingVideo = false;
        this.videoUrl = '';
      } else {
        // 如果没有观看视频，则开始定时请求
        this.startVideo();
      }
    },
    async startVideo() {
      try {
        const response = await fetch('http://localhost:5000/fire_monitor', {
          method: 'GET',
          // 可能需要包含身份验证标头或其他参数
        });
        if (response.ok) {
          this.watchingVideo = true;
          this.intervalId = setInterval(this.getVideoFrame, 100); // 每秒获取10帧图片
        } else {
          console.error('Failed to start video stream');
        }
      } catch (error) {
        console.error('Error starting video stream:', error);
      }
    },
    async getVideoFrame() {
      // try {
      //   const response = await fetch('http://localhost:5000/fire_monitor', {
      //     method: 'GET',
      //     // 可能需要包含身份验证标头或其他参数
      //   });
      //   if (response.ok) {
      //     const imageData = await response.blob();
      //     this.videoUrl = URL.createObjectURL(imageData); // 使用Blob URL显示图片
      //   } else {
      //     console.error('Failed to get video frame');
      //   }
      // } catch (error) {
      //   console.error('Error getting video frame:', error);
      // }
      const imageData = await response.blob();
      this.videoUrl = URL.createObjectURL(imageData); // 使用Blob URL显示图片
    },
  },
  beforeUnmount() {
    // 组件销毁时清除定时器和释放资源
    clearInterval(this.intervalId);
    URL.revokeObjectURL(this.videoUrl);
  },
};
</script>
