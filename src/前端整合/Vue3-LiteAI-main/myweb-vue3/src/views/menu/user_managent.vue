<script setup lang="ts">
import { useMenus } from '@/composables/useMenus'
import { useRouter } from 'vue-router'
import { getFaceById } from '@/api/menus'
import { b64toBlob } from '@/components/layout/Blob_convter'

const router = useRouter()
const { allMenus, getAllMenus, handleDelete } = useMenus()
const base64str = ref('')
const imgURL = ref('')
const isDialogVisible = ref(false)
const handleShow = async (id: string) => {
  const { data } = await getFaceById(id)
  const blob = b64toBlob(data.message)
  imgURL.value = window.URL.createObjectURL(blob)
  console.log(imgURL.value)
  isDialogVisible.value = true;
}

const addUser = () => {
  router.push('/lpdr')
}
getAllMenus()
</script>

<template>
  <el-dialog v-model="isDialogVisible" title="查看人脸" width="550">
    <img :src="imgURL" width="500" />
  </el-dialog>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h3>用户信息表</h3>
      </div>
    </template>
    <el-table :data="allMenus" border style="width: 100%">
      <el-table-column type="index" label="序号" align="center" width="60px" />
      <el-table-column prop="identity" label="身份" align="center" width="100px" />
      <el-table-column prop="username" label="账号" align="center" width="140px" />
      <el-table-column prop="password" label="密码" align="center" width="140px" />
      <el-table-column prop="token" label="令牌" align="center" />
      <el-table-column label="操作" align="center" width="200px" v-slot="scope">
        <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        <el-button type="primary" @click="handleShow(scope.row.id)">查看</el-button>
      </el-table-column>
    </el-table>
    <div class="buttonBox"> <el-button @click="addUser">添加用户</el-button></div>
  </el-card>
</template>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: auto;
}

.buttonBox {
  width: auto;
  display: flex;
  justify-content: center;
  margin-top: 10px;
}
</style>
