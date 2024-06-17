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

<!-- 
  2024年6月11日12:39:30
  无美术版本的监控界面
 -->
<!-- <template>
  <div>
    <h1>视频监控系统</h1>
    <img :src="videoSrc_smoke" alt="Video Stream">
    <img :src="videoSrc_person" alt="Video Stream">
    <button @click="startVideoStream_smoke">开启烟雾监控</button>
    <button @click="stopVideoStream_smoke">停止烟雾监控</button>
    <button @click="startVideoStream_person">开启陌生人监控</button>
    <button @click="stopVideoStream_person">停止陌生人监控</button>
    <button @click="navigateToHome">返回主页</button>
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
    },
    navigateToHome() {
      window.location.href = 'http://localhost:5173';
    }
  }
};
</script>

<style>
/* 样式可以根据需求自行调整 */
</style> -->

<template>
  <div class="container">
    <h1>视频监控系统</h1>
    <div class="video-container">
      <img :src="videoSrc_smoke" alt="Video Stream">
      <img :src="videoSrc_person" alt="Video Stream">
    </div>
    <div class="button-container">
      <button @click="startVideoStream_smoke" class="btn start">开启烟雾监控</button>
      <button @click="stopVideoStream_smoke" class="btn stop">停止烟雾监控</button>
      <button @click="startVideoStream_person" class="btn start">开启陌生人监控</button>
      <button @click="stopVideoStream_person" class="btn stop">停止陌生人监控</button>
      <button @click="navigateToHome" class="btn home">返回主页</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      videoSrc_smoke: '',
      videoSrc_person: ''
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
          this.videoSrc_smoke = `http://localhost:5000/fire_monitor?_t=${randomParam}`;
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
          this.videoSrc_person = `http://localhost:5000/person_monitor?_t=${randomParam}`;
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
    },
    navigateToHome() {
      window.location.href = 'http://localhost:5173';
    }
  }
};
</script>

<style>
.container {
  text-align: center;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.video-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.video-container img {
  max-width: 45%;
  margin: 0 10px;
  border: 2px solid #ccc;
  border-radius: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 10px 20px;
  margin: 5px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s;
  cursor: pointer;
}

.btn:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

.btn.start {
  background-color: #4CAF50;
}

.btn.start:hover {
  background-color: #45a049;
}

.btn.stop {
  background-color: #f44336;
}

.btn.stop:hover {
  background-color: #e53935;
}

.btn.home {
  background-color: #008CBA;
}

.btn.home:hover {
  background-color: #007bb5;
}
</style>