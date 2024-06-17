<script setup lang="ts">
import type { FormInstance, FormRules, UploadFile, UploadInstance, UploadProps } from 'element-plus'
import { b64toBlob } from '@/components/layout/Blob_convter'
import { addUser } from '@/api/users'

const imageUrl = ref('')
const img_infer = ref('')
const rec_result = ref('')
const isLoading = ref(false)
const form = reactive({
  username: '',
  password: '',
  base64str: '',
  identity: false
})

const convertToBase64 = async () => {
  try {
    const response = await fetch(imageUrl.value);
    const blob = await response.blob();
    const reader = new FileReader();
    reader.onload = (e: any) => {
      form.base64str = e.target.result;
      form.base64str = form.base64str.replace(/\+/g, "%2B");
    };
    reader.readAsDataURL(blob);
  } catch (error: any) {
    ElMessage.error('图片加载失败：' + error.message);
  }
}

const justSelect = (uploadFile: UploadFile) => {
  imageUrl.value = URL.createObjectURL(uploadFile.raw!)
  convertToBase64();
}

const handleSuccess = (response: any) => {
  if (response.success) {
    const blob = b64toBlob(response.content.img_data)
    img_infer.value = window.URL.createObjectURL(blob)
    rec_result.value = response.content.rec_result
  } else {
    ElMessage.error(response.message)
  }
}
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}

const onSubmit = async () => {
  isLoading.value = true
  await formRef.value?.validate().catch((err: any) => {
    ElMessage.error('表单校验失败...')
    isLoading.value = false
    throw err
  })
  const data = await addUser(form).then((res) => {
    if (!res.data.success) {
      ElMessage.error(res.data.message)
      isLoading.value = false
      throw new Error(res.data.message)
    }
    return res.data
  })
  isLoading.value = false
  ElMessage.success('注册成功!')
}

const uploadRef = ref<UploadInstance>()
const formRef = ref<FormInstance>()
const rules = reactive<FormRules>({
  username: [
    { required: true, message: '用户名不能为空', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度需要2~20位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 18, message: '密码长度需要6~18位', trigger: 'blur' }
  ]
})
</script>

<template>
  <el-card>
    <template #header>
      <h3>添加家庭成员</h3>
    </template>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="auto" style="max-width: 600px">
      <el-form-item label="用户名">
        <el-input v-model="form.username" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" clearable placeholder="请输入密码" show-password></el-input>
      </el-form-item>
      <el-form-item label="是否为管理员">
        <el-switch v-model="form.identity" />
      </el-form-item>
      <el-form-item label="上传人脸">
        <el-upload ref="uploadRef" class="avatar-uploader" action="/users/upload/" :show-file-list="false"
          :on-change="justSelect" :before-upload="beforeAvatarUpload" drag :data="{ data: 'lpdr' }" :auto-upload="false"
          :on-success="handleSuccess">
          <img v-if="imageUrl" :src="imageUrl" class="avatar" />
          <el-icon v-else class="el-icon--upload" size="50"><IEpupload-filled /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label=" ">
        <el-button type="primary" @click="onSubmit" :loading="isLoading">创建</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<style scoped>
.avatar-uploader .avatar {
  width: 350px;
  height: 350px;
  object-fit: contain;
}

.avatar-uploader img {
  justify-content: center;
  align-items: center;
}
</style>

<style lang="scss" scoped>
.avatar-uploader .el-upload {
  border: 3px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.el-icon--upload {
  font-size: 28px;
  color: #8c939d;
  height: 50px;
  width: 100px;
  text-align: center;
  justify-content: center;
}

.result-demo {
  width: 410px;
  height: 434px;
  display: flex;
  border: 1px dashed var(--el-border-color);
  justify-content: center;
  align-items: center;
}

.result-demo img {
  width: 95%;
  height: 80%;
  display: block;
  object-fit: contain;
}

.rec_res {
  width: 410px;
  height: 434px;
  display: flex;
  border: 1px dashed var(--el-border-color);
}
</style>
