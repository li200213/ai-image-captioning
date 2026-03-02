<template>
  <div class="login-container">
    
    <!-- ================== 左侧：产品介绍区域 ================== -->
    <div class="intro-section">
      <div class="intro-content">
        <h1 class="app-title">智能看图配文系统</h1>
        
        <div class="pain-point">
          <p>“ 每次发朋友圈，照片选好了，</p>
          <p>却总是不知道该配什么文案？ ”</p>
        </div>

        <div class="solution">
          <p>在这里，让 AI 懂你的图，更懂你的心。</p>
          <ul class="features">
            <li>✨ <strong>一键生成</strong>：上传图片，秒出文案</li>
            <li>🎨 <strong>多场景</strong>：朋友圈、小红书、现代诗</li>
            <li>❤️ <strong>懂情绪</strong>：开心、忧伤、平静，随心切换</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ================== 右侧：登录/注册表单 ================== -->
    <div class="form-section">
      <el-card class="auth-card">
        <template #header>
          <div class="card-header">
            <span>用户登录</span>
          </div>
        </template>
        
        <el-form :model="form" label-width="0"> <!-- label-width设为0，靠内部div居中 -->
          <el-form-item>
            <el-input 
              v-model="form.username" 
              placeholder="请输入用户名" 
              :prefix-icon="User" 
              size="large"
            />
          </el-form-item>
          
          <el-form-item>
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码" 
              show-password
              maxlength="12"
              :prefix-icon="Lock" 
              size="large"
            />
          </el-form-item>
          
          <!-- 按钮居中修正版 -->
          <el-form-item>
            <div style="width: 100%; display: flex; justify-content: center;">
              <el-button 
                type="primary" 
                @click="handleLogin" 
                :loading="loading" 
                style="width: 100%;" 
                size="large"
              >
                立即登录
              </el-button>
            </div>
          </el-form-item>

          <div class="auth-links">
            <el-link type="primary" @click="$router.push('/register')">
              还没有账号？免费注册
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
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('账号和密码不能为空')
    return
  }

  // 密码校验规则（保持你之前的逻辑）
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

    const response = await axios.post('http://127.0.0.1:5000/api/login', formData)

    if (response.data.code === 200) {
      ElMessage.success('登录成功！')
      localStorage.setItem('username', form.username)
      router.push('/home')
    } else {
      ElMessage.error(response.data.message || '登录失败')
    }

  } catch (error) {
    console.error(error)
    ElMessage.error('无法连接到服务器')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 全屏大容器：Flex 左右布局 */
.login-container {
  display: flex;
  height: 100vh; /* 占满全屏高度 */
  width: 100vw;
  background-color: #f0f2f5;
  overflow: hidden;
}

/* --- 左侧：介绍区域 --- */
.intro-section {
  flex: 1; /* 占据剩余空间 (约60%宽度) */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* 漂亮的蓝紫渐变 */
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  padding: 40px;
  position: relative;
}

/* 装饰背景图案 (可选) */
.intro-section::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(white 1px, transparent 1px);
  background-size: 30px 30px;
  opacity: 0.1;
}

.intro-content {
  max-width: 500px;
  z-index: 1;
}

.app-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 40px;
  letter-spacing: 2px;
  text-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.pain-point {
  font-size: 1.5rem;
  font-style: italic;
  margin-bottom: 30px;
  line-height: 1.6;
  opacity: 0.9;
  border-left: 4px solid rgba(255,255,255,0.5);
  padding-left: 20px;
}

.solution {
  font-size: 1.1rem;
  background: rgba(255, 255, 255, 0.1); /* 半透明背景 */
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
  margin-bottom: 10px;
  font-size: 1rem;
}

/* --- 右侧：表单区域 --- */
.form-section {
  width: 500px; /* 固定宽度 */
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: -5px 0 20px rgba(0,0,0,0.05);
}

.auth-card {
  width: 380px;
  border: none; /* 去掉卡片边框，更融合 */
  box-shadow: none !important; /* 去掉卡片阴影，由外层控制 */
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
  margin-top: 15px;
}

/* 响应式：手机端时上下排列 */
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
  .solution { display: none; } /* 手机端隐藏详细列表 */
  .form-section {
    width: 100%;
    flex: 1;
    border-radius: 20px 20px 0 0; /* 手机端做个圆角 */
    margin-top: -20px;
    z-index: 2;
  }
}
</style>