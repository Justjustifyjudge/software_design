<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { login, loginByFace } from '@/api/users'
import { useTokenStore } from '@/stores/mytoken'
import { useRouter } from 'vue-router'

let stream: MediaStream | null = null
const video = ref();
const canvas = ref();
const isCameraOn = ref(false);
const isDialogVisible = ref(false);
const store = useTokenStore()
const router = useRouter()
const form = reactive({
    username: '',
    password: '',
    base64str: ''
})

//人脸识别登录
const start = () => {
    isDialogVisible.value = true;
    startCamera();
}

const stop = () => {
    stopCamera();
    isDialogVisible.value = false;
}

//打开摄像头
const startCamera = async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.value.srcObject = stream;
        video.value.play();
        isCameraOn.value = true;
    } catch (error) {
        console.error('Something went wrong!', error);
    }
};

//关闭摄像头
const stopCamera = () => {
    if (stream) {
        stream.getTracks().forEach((track: { stop: () => any }) => track.stop());
        stream = null;
    }
};

//拍照
const takePhoto = () => {
    const context = canvas.value.getContext('2d');
    if (video.value.readyState === video.value.HAVE_ENOUGH_DATA) {
        context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);
        form.base64str = canvas.value.toDataURL('image/png');
        form.base64str = form.base64str.replace(/\+/g, "%2B");
    }
};

//提交表单
const onSubmit = async () => {
    isLoading.value = true
    await formRef.value?.validate().catch((err: any) => {
        ElMessage.error('表单校验失败...')
        isLoading.value = false
        throw err
    })
    const data = await login(form).then((res) => {
        if (!res.data.success) {
            ElMessage.error(res.data.message)
            isLoading.value = false
            throw new Error(res.data.message)
        }
        return res.data
    })
    store.saveToken(data.content)

    isLoading.value = false

    ElMessage.success('登录成功!')

    if (store.token.identity == '超级管理员') {
        router.push('/')
    } else {
        router.push('/user_look')
    }
}

const sendPhoto = async () => {
    const data = await loginByFace(form).then((res) => {
        if (!res.data.success) {
            ElMessage.error('登录失败，人脸未识别！')
            isLoading.value = false
            throw new Error('登录失败，人脸未识别！')
        }
        return res.data
    })
    store.saveToken(data.content)
    ElMessage.success('登录成功!')
    stopCamera()
    if (store.token.identity == '超级管理员') {
        router.push('/')
    } else {
        router.push('/user_look')
    }
}

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

const isLoading = ref(false)
const formRef = ref<FormInstance>()
</script>

<template>
    <div class="body">
        <el-dialog v-model="isDialogVisible" :before-close="stop" title="人脸录取" width="700">
            <div class="showArea">
                <video ref="video" width="640" autoplay></video>
                <canvas ref="canvas" width="640" height="480"></canvas>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="takePhoto">
                        拍照
                    </el-button>
                    <el-button type="primary" @click="sendPhoto"> 确认 </el-button>
                </div>
            </template>
        </el-dialog>
        <div class="content">
            <div class="introduce">
                <div class="introduce-content">
                    <p class="tips animate__animated animate__slideInLeft">
                        家庭安全监控系统
                    </p>
                </div>
            </div>
            <div class="form-wrapper animate__animated animate__slideInRight">
                <div class="login-form">
                    <h1>Login</h1>
                    <div class="other-login" @click="start">
                        <span>人脸识别登录</span>
                    </div>
                    <div class="divider">
                        <span class="line"></span>
                        <span class="divider-text">账号密码登录</span>
                        <span class="line"></span>
                    </div>
                    <div class="form">
                        <el-form :model="form" :rules="rules" ref="formRef">
                            <el-form-item prop="username">
                                <span class="input-tips">Username</span>
                                <el-input v-model="form.username" clearable placeholder="请输入家庭成员账号"></el-input>
                            </el-form-item>
                            <el-form-item prop="password">
                                <span class="input-tips">Password</span>
                                <el-input v-model="form.password" clearable placeholder="请输入密码"
                                    show-password></el-input>
                            </el-form-item>
                        </el-form>
                        <el-button type="primary" @click="onSubmit" :loading="isLoading">Login</el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
@charset "UTF-8";

@font-face {
    font-family: Butler_Light;
    font-weight: 700;
    src: url(../../assets/font/Butler_Light.otf) format("truetype");
    text-rendering: optimizeLegibility;
}

* {
    padding: 0;
    margin: 0;
    font-family: Butler_Light;
}

.body {
    background-image: url(../../assets/bg.jpg);
    background-attachment: fixed;
    background-size: cover;
    color: #fff;
}

.content {
    width: 100vw;
    height: 100vh;
    position: relative;
    display: flex;
    overflow: hidden;
}

.content .introduce {
    width: 50%;
    height: 100%;
    position: relative;
    position: relative;
}

.content .introduce .introduce-content .tips {
    margin: 20px 0;
    font-size: 25px;
    position: absolute;
    left: 30%;
    top: 40%;
    transform: translateY(-50%);
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-weight: 800;
    text-shadow: 2px 2px 2px #000;
    font-size: 50px;
}

.content .form-wrapper {
    width: 50%;
    height: 100%;
    position: absolute;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20% 10%;
    box-sizing: border-box;
    background: rgba(0, 0, 0, 0.06);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

.content .form-wrapper .login-form {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.content .form-wrapper .login-form h1 {
    font-size: 55px;
    margin-bottom: 5px;
}

.login-tips {
    font-size: 20px;
}

.other-login {
    width: 100%;
    height: 50px;
    line-height: 50px;
    border: 1px solid #fff;
    text-align: center;
    border-radius: 10px;
    box-sizing: border-box;
    margin: 50px 0 10px 0;
    cursor: pointer;
    transition: 0.2s;
}

.content .form-wrapper .login-form .other-login:hover {
    border: 1px solid #9faff8;
}

img {
    width: 30px;
    height: 30px;
    vertical-align: middle;
}

.content .form-wrapper .login-form .other-login span {
    vertical-align: middle;
}

.content .form-wrapper .login-form .divider {
    width: 100%;
    margin: 20px 0;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.content .form-wrapper .login-form .divider .line {
    display: inline-block;
    flex: 1;
    height: 1px;
    background-color: #fff;
}

span {
    display: inline-block;
    margin-bottom: 5px;
}

.ipt:focus {
    border: 1px solid #9faff8;
}

.content .form-wrapper .login-form {
    color: #fff;
    cursor: pointer;
}

:deep(.el-input__inner) {
    width: 100%;
    height: 100%;
    border-radius: 10px;
    border: 1px solid #fff;
    padding: 10px 0 10px 30px;
    box-sizing: border-box;
    background-color: transparent;
    outline: none;
    font-size: 20px;
    color: rgb(44, 50, 57);
    font-family: Butler_Light;
}

:deep(.el-button) {
    width: 100%;
    height: 50px;
    border: 0;
    background-image: linear-gradient(to right, rgb(112, 103, 118), rgb(80, 60, 80));
    border-radius: 5px;
    color: #000;
    text-align: center;
    margin: 50px 0;
    font-size: 20px;
    cursor: pointer;
}

:deep(.el-button):hover {
    border: 3px solid rgb(22, 45, 144);
}

:deep(.el-dialog__body) {
    background-image: url(../../assets/bg.jpg);
    background-attachment: fixed;
    background-size: cover;
}
</style>
