<template>
  <div class="login-container">
    
    <!-- ================== 左侧：欢迎加入区域 ================== -->
    <div class="intro-section">
      <div class="intro-content">
        <h1 class="app-title">智能看图配文系统</h1>
        
        <div class="pain-point">
          <p>“ 加入我们，</p>
          <p>让每一张照片都拥有灵魂。 ”</p>
        </div>

        <div class="solution">
          <p>只需三步，开启 AI 创作之旅：</p>
          <ul class="features">
            <li>1️⃣ <strong>注册账号</strong>：建立你的专属创作空间</li>
            <li>2️⃣ <strong>上传美图</strong>：支持批量上传，九宫格预览</li>
            <li>3️⃣ <strong>一键生成</strong>：获取高赞朋友圈文案</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ================== 右侧：注册表单 ================== -->
    <div class="form-section">
      <el-card class="auth-card">
        <template #header>
          <div class="card-header">
            <span>注册新账号</span>
          </div>
        </template>
        
        <el-form :model="form" label-width="0">
          
          <!-- 用户名 -->
          <el-form-item>
            <el-input 
              v-model="form.username" 
              placeholder="请设置用户名" 
              :prefix-icon="User" 
              size="large"
            />
          </el-form-item>
          
          <!-- 密码 -->
          <el-form-item>
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="设置密码 (6-12位，含字母数字)" 
              show-password
              maxlength="12"
              :prefix-icon="Lock" 
              size="large"
            />
          </el-form-item>

          <!-- 确认密码 -->
          <el-form-item>
            <el-input 
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="请再次确认密码" 
              show-password
              maxlength="12"
              :prefix-icon="Lock" 
              size="large"
            />
          </el-form-item>
          
          <!-- 注册按钮 -->
          <el-form-item>
            <div style="width: 100%; display: flex; justify-content: center;">
              <el-button 
                type="success" 
                @click="handleRegister" 
                :loading="loading" 
                style="width: 100%;" 
                size="large"
              >
                立即注册
              </el-button>
            </div>
          </el-form-item>

          <!-- 返回登录链接 -->
          <div class="auth-links">
            <el-link type="primary" @click="$router.push('/')">
              已有账号？返回登录
            </el-link>
          </div>

        </el-form>
      </el-card>
    </div>

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  // 1. 基础非空校验
  if (!form.username || !form.password || !form.confirmPassword) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  // 2. 密码一致性校验
  if (form.password !== form.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  // 3. 密码复杂度校验 (可选，保持和登录页一致)
  if (form.password.length > 12) {
    ElMessage.warning('密码长度不能超过12位')
    return
  }
  const regex = /^(?=.*[A-Za-z])(?=.*\d).+$/
  if (!regex.test(form.password)) {
    ElMessage.warning('密码必须同时包含字母和数字')
    return
  }

  loading.value = true

  try {
    const formData = new FormData()
    formData.append('username', form.username)
    formData.append('password', form.password)
    
    // 发送注册请求
    const res = await axios.post('http://127.0.0.1:5000/api/register', formData)
    
    if (res.data.code === 200) {
      ElMessage.success('注册成功，请登录！')
      // 注册成功后跳回登录页
      router.push('/')
    } else {
      ElMessage.error(res.data.message || '注册失败，用户名可能已存在')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('服务器连接失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 复用 Login 页面的 CSS 布局 */

/* 全屏大容器 */
.login-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #f0f2f5;
  overflow: hidden;
}

/* --- 左侧：介绍区域 --- */
.intro-section {
  flex: 1; 
  /* 这里换一个稍微不同的渐变色，区分登录页 */
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  padding: 40px;
  position: relative;
}

/* 装饰背景 */
.intro-section::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(white 1px, transparent 1px);
  background-size: 30px 30px;
  opacity: 0.15;
}

.intro-content {
  max-width: 500px;
  z-index: 1;
}

.app-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 40px;
  text-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.pain-point {
  font-size: 1.5rem;
  font-style: italic;
  margin-bottom: 30px;
  line-height: 1.6;
  opacity: 0.95;
  border-left: 4px solid rgba(255,255,255,0.6);
  padding-left: 20px;
}

.solution {
  font-size: 1.1rem;
  background: rgba(255, 255, 255, 0.15);
  padding: 25px;
  border-radius: 12px;
  backdrop-filter: blur(5px);
}

.features {
  list-style: none;
  padding: 0;
  margin-top: 15px;
}

.features li {
  margin-bottom: 12px;
  font-size: 1rem;
}

/* --- 右侧：表单区域 --- */
.form-section {
  width: 500px;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: -5px 0 20px rgba(0,0,0,0.05);
}

.auth-card {
  width: 380px;
  border: none;
  box-shadow: none !important;
}

.card-header {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.auth-links {
  text-align: center;
  margin-top: 20px;
}

/* 响应式适配 */
@media (max-width: 900px) {
  .login-container {
    flex-direction: column;
  }
  .intro-section {
    flex: 0.4;
    padding: 20px;
  }
  .app-title { font-size: 2rem; margin-bottom: 15px; }
  .pain-point { font-size: 1.1rem; }
  .solution { display: none; }
  .form-section {
    width: 100%;
    flex: 1;
    border-radius: 20px 20px 0 0;
    margin-top: -20px;
    z-index: 2;
  }
}
</style>