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
    <img :src="videoSrc_smoke" alt="Video Stream">
    <img :src="videoSrc_person" alt="Video Stream">
    <button @click="startVideoStream_smoke">开启烟雾监控</button>
    <button @click="stopVideoStream_smoke">停止烟雾监控</button>
    <button @click="startVideoStream_person">开启陌生人监控</button>
    <button @click="stopVideoStream_person">停止陌生人监控</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      videoSrc_smoke: '',
      videoSrc_preson: ''
    };
  },
  mounted() {
    this.startVideoStream_smoke();
    this.startVideoStream_person();
  },
  methods: {
    startVideoStream_smoke() {
      fetch('http://localhost:5000/start_streaming_smoke')
        .then(response => response.text())
        .then(data => {
          console.log(data);  // 打印服务器返回的信息
          let randomParam = Math.random();  // 随机参数，防止缓存
          this.videoSrc_smoke = 'http://localhost:5000/fire_monitor?_t=${randomParam}';
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    stopVideoStream_smoke() {
      fetch('http://localhost:5000/stop_streaming_smoke')
        .then(response => response.text())
        .then(data => {
          console.log(data);  // 打印服务器返回的信息
          this.videoSrc_smoke = '';
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    startVideoStream_person() {
      fetch('http://localhost:5000/start_streaming_person')
        .then(response => response.text())
        .then(data => {
          console.log(data);  // 打印服务器返回的信息
          let randomParam = Math.random();  // 随机参数，防止缓存
          this.videoSrc_person = 'http://localhost:5000/person_monitor?_t=${randomParam}';
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    stopVideoStream_person() {
      fetch('http://localhost:5000/stop_streaming_person')
        .then(response => response.text())
        .then(data => {
          console.log(data);  // 打印服务器返回的信息
          this.videoSrc_person = '';
        })
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

