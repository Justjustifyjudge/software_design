<script setup lang="ts">
import { isCollapse } from './isCollapse'
</script>

<template>
  <el-aside>
    <el-scrollbar>
      <el-menu router :collapse="isCollapse" background-color="#545c64">
        <a href="/" class="logo">
          <svg t="1717225032491" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="1732" width="30" height="30">
            <path
              d="M512 0C229.229714 0 0 229.229714 0 512s229.229714 512 512 512 512-229.229714 512-512S794.770286 0 512 0z m61.169371 642.925714l24.641829 143.557486c2.925714 16.822857-7.511771 32.738743-21.460114 32.738743H447.634286c-13.948343 0-24.349257-15.879314-21.460115-32.738743L450.830629 642.925714c-93.622857-26.594743-162.143086-112.705829-162.143086-214.8352C288.687543 304.764343 388.666514 204.8 512 204.8s223.312457 99.986286 223.312457 223.312457c0 102.107429-68.549486 188.218514-162.143086 214.813257z"
              fill="#3D3D3D" p-id="1733"></path>
            <path
              d="M450.830629 642.925714l-24.641829 143.557486C423.299657 803.342629 433.737143 819.2 447.634286 819.2h128.731428c13.948343 0 24.356571-15.879314 21.460115-32.738743L573.169371 642.925714a224.928914 224.928914 0 0 1-122.338742 0z"
              fill="#645E9E" p-id="1734"></path>
            <path
              d="M512 204.8c-123.333486 0-223.312457 99.986286-223.312457 223.312457 0 102.129371 68.549486 188.240457 162.143086 214.8352a224.928914 224.928914 0 0 0 122.338742 0c93.622857-26.594743 162.143086-112.705829 162.143086-214.8352C735.312457 304.764343 635.333486 204.8 512 204.8z m0 60.708571a21.942857 21.942857 0 1 1-21.942857 21.942858 21.942857 21.942857 0 0 1 21.942857-21.942858z m0 319.217372a109.714286 109.714286 0 1 1 109.714286-109.714286 109.714286 109.714286 0 0 1-109.714286 109.685029z"
              fill="#8A78CE" p-id="1735"></path>
            <path
              d="M512 365.268114a109.714286 109.714286 0 1 0 109.714286 109.714286 109.714286 109.714286 0 0 0-109.714286-109.714286z m0 198.473143c-48.610743 0-88.020114-39.738514-88.020114-88.758857S463.389257 386.194286 512 386.194286s88.020114 39.738514 88.020114 88.766171S560.610743 563.741257 512 563.741257z"
              fill="#9D8FD1" p-id="1736"></path>
            <path
              d="M423.979886 474.9824a88.758857 88.020114 90 1 0 176.040228 0 88.758857 88.020114 90 1 0-176.040228 0Z"
              fill="#FFFFFF" p-id="1737"></path>
            <path
              d="M512 287.422171m-21.942857 0a21.942857 21.942857 0 1 0 43.885714 0 21.942857 21.942857 0 1 0-43.885714 0Z"
              fill="#FFFFFF" p-id="1738"></path>
          </svg>
          <h1>家庭安全监控系统</h1>
        </a>
        <el-menu-item index="/">
          <el-icon>
            <IEpMonitor />
          </el-icon><span> 工作台 </span>
        </el-menu-item>
        <el-menu-item index="/user_menu">
          <el-icon>
            <IEpLock />
          </el-icon> <span> 家庭成员账户管理 </span>
        </el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <el-icon style="color: white">
              <IEpPromotion />
            </el-icon>
            <span style="color: white"> 人脸管理 </span>
          </template>
          <el-menu-item index="/ocr">
            <el-icon>
              <IEpPear />
            </el-icon> <span> 陌生人脸管理 </span>
          </el-menu-item>
          <el-menu-item index="/lpdr">
            <el-icon>
              <IEpGrape />
            </el-icon> <span> 添加家庭成员 </span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </el-aside>
</template>

<style lang="scss" scoped>
@charset "UTF-8";

@font-face {
  font-family: Butler_Light;
  font-weight: 700;
  src: url(../../assets/font/Butler_Light.otf) format("truetype");
  text-rendering: optimizeLegibility;
}

.el-aside {
  background-color: #545c64;
  height: 100vh;
  width: auto;
}

.el-menu {
  border-right: none;
  width: 200px;

  &.el-menu--collapse {
    width: 60px;

    & h1 {
      display: none;
    }
  }

  .el-menu-item {
    color: white;
  }
}

.logo {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Georgia, 'Times New Roman', Times, serif;
  font-weight: 800;
  height: 60px;
  text-decoration: none;
  color: white;
  background-color: #545c64;

  img {
    width: 32px;
    height: 32px;
  }
}
</style>
