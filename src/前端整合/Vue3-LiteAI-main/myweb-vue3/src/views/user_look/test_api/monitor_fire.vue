<!-- <template>
  <div>
    <button @click="startVideo">查看视频</button>
    <button @click="stopVideo">退出</button>
    <video v-if="showVideo" ref="video" controls autoplay></video>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showVideo: false,
      videoSrc: 'http://localhost:5000/fire_monitor',  // 后端接口地址
      intervalId: null,
    };
  },
  methods: {
    startVideo() {
      this.showVideo = true;
      this.intervalId = setInterval(() => {
        this.$refs.video.src = this.videoSrc + `?_t=${new Date().getTime()}`;
      }, 1000);  // 每秒更新一次图片
    },
    stopVideo() {
      this.showVideo = false;
      clearInterval(this.intervalId);
      this.$refs.video.src = '';
    },
  },
};
</script> -->


<!-- <template>
  <div>
    <h1>视频监控系统</h1>
    <img :src="videoSrc" alt="Video Stream">
  </div>
</template>

<script>
export default {
  data() {
    return {
      videoSrc: ''
    };
  },
  mounted() {
    this.startVideoStream();
  },
  methods: {
    startVideoStream() {
      this.videoSrc = 'http://localhost:5000/fire_monitor';
    }
  }
};
</script>

<style>
/* 样式可以根据需求自行调整 */
</style> -->


<template>
  <div>
    <h1>视频监控系统</h1>
    <img :src="videoSrc" alt="Video Stream">
    <button @click="startVideoStream">开启视频流</button>
    <button @click="stopVideoStream">停止视频流</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      videoSrc: ''
    };
  },
  mounted() {
    this.startVideoStream();
  },
  methods: {
    startVideoStream() {
      fetch('http://localhost:5000/start_streaming')
        .then(response => response.text())
        .then(data => {
          console.log(data);  // 打印服务器返回的信息
          let randomParam = Math.random();  // 随机参数，防止缓存
          this.videoSrc = 'http://localhost:5000/fire_monitor?_t=${randomParam}';
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    stopVideoStream() {
      fetch('http://localhost:5000/stop_streaming')
        .then(response => response.text())
        .then(data => {
          console.log(data);  // 打印服务器返回的信息
        })
        .then(this.videoSrc = '')
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }
};
</script>

<style>
/* 样式可以根据需求自行调整 */
</style>

