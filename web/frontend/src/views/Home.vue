<template>
  <div class="home-container">
    
    <!-- ================== 1. 顶部导航栏 ================== -->
    <!-- 样式由 assets/header.css (或 common-layout.css) 控制 -->
    <div class="header">
      <div class="logo">
        智能看图配文系统
      </div>

      <div class="user-area">
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">
            <el-avatar :size="32" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <span class="username">{{ username }}</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="history" :icon="Clock">历史记录</el-dropdown-item>
              <el-dropdown-item command="logout" :icon="SwitchButton" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- ================== 2. 主体内容区域 ================== -->
    <div class="main-content">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>✨ 开始创作</span>
          </div>
        </template>

        <!-- 2.1 图片上传区域 -->
        <div class="section">
          <h3>第一步：上传图片（最多9张）</h3>
          <!-- 
             新增 :on-preview="handlePictureCardPreview" 
             用于点击放大镜时触发
          -->
          <el-upload
            v-model:file-list="fileList"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :limit="9"
            :on-change="handleChange"
            :on-exceed="handleExceed"
            :on-preview="handlePictureCardPreview"
            multiple
          >
            <el-icon><Plus /></el-icon>
          </el-upload>

          <!-- 新增：图片预览弹窗 -->
          <el-dialog v-model="dialogVisible" title="图片预览" width="50%">
            <img :src="dialogImageUrl" alt="Preview Image" style="width: 100%; height: auto;" />
          </el-dialog>
        </div>

        <!-- 2.2 选项区域 -->
        <div class="section">
          <h3>第二步：选择要求</h3>
          
          <div class="option-row">
            <span class="label">配文风格：</span>
            <el-radio-group v-model="style">
              <el-radio label="朋友圈">朋友圈</el-radio>
              <el-radio label="小红书">小红书</el-radio>
              <el-radio label="现代诗">现代诗</el-radio>
            </el-radio-group>
          </div>
          
          <div class="option-row">
            <span class="label">情绪色彩：</span>
            <el-radio-group v-model="emotion">
              <el-radio label="开心">开心</el-radio>
              <el-radio label="忧伤">忧伤</el-radio>
              <el-radio label="平静">平静</el-radio>
            </el-radio-group>
          </div>
        </div>

        <!-- 2.3 运行按钮 -->
        <div class="action-area">
          <el-button type="primary" size="large" @click="submitUpload" :loading="loading" style="width: 200px;">
            {{ loading ? 'AI 正在思考中...' : '开始生成配文' }}
          </el-button>
        </div>

        <!-- 2.4 结果展示 -->
        <div v-if="resultData" class="result-box">
          <h4>🎉 生成结果：</h4>
          <div class="result-content">
            {{ resultData }}
          </div>
          <div class="result-footer">
            <el-button type="success" link @click="copyText(resultData)">复制文案</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ArrowDown, SwitchButton, Clock, Plus } from '@element-plus/icons-vue'

const router = useRouter()

// --- 状态变量 ---
const username = ref('未登录')
const fileList = ref([])      // 图片列表
const style = ref('朋友圈')    // 风格
const emotion = ref('开心')    // 情绪
const loading = ref(false)    // 加载状态
const resultData = ref('')    // 存放结果文本

// --- 新增：图片预览相关变量 ---
const dialogImageUrl = ref('')
const dialogVisible = ref(false)



// --- 顶部菜单处理 ---
const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('username')
    ElMessage.success('退出成功')
    router.push('/')
  } else if (command === 'history') {
    router.push('/history')
  }
}

// --- 上传组件逻辑 ---
const handleChange = (uploadFile, uploadFiles) => {
  fileList.value = uploadFiles
}

const handleExceed = () => {
  ElMessage.warning('最多只能上传 9 张图片哦！')
}

// --- 新增：处理图片预览 ---
const handlePictureCardPreview = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url
  dialogVisible.value = true
}

// --- 核心：提交给 Flask ---
const submitUpload = async () => {
  if (fileList.value.length === 0) {
    ElMessage.error('请至少上传一张图片')
    return
  }

  loading.value = true
  resultData.value = ''

  const formData = new FormData()
  fileList.value.forEach((file) => {
    formData.append('imgFile_list', file.raw) 
  })
  formData.append('text_type', style.value)
  formData.append('emotion_type', emotion.value)
  formData.append('username', username.value)

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/generate', formData)
    
    if(response.data.code === 200) {
      resultData.value = response.data.data
      ElMessage.success('生成成功！')
    } else {
      ElMessage.error('生成失败：' + response.data.message)
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('服务器连接失败，请检查后端是否启动')
  } finally {
    loading.value = false
  }
}

// 小功能：复制文本
const copyText = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}
</script>

<style scoped>
/* 引入公共样式 (导航栏等) */
/* 请确保 src/assets/header.css 或 common-layout.css 存在 */
@import '../assets/header.css'; 

/* --- 修复并统一后的 CSS --- */

/* 卡片容器 */
.box-card { 
  max-width: 900px; 
  margin: 0 auto; 
  border-radius: 8px;
}

/* 卡片头部 */
.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

/* 每个步骤区块 */
.section { 
  margin-bottom: 30px; 
}

/* 步骤标题 */
.section h3 { 
  margin-bottom: 15px; 
  border-left: 4px solid #409EFF; 
  padding-left: 10px; 
  font-size: 16px; 
  color: #303133;
}

/* 选项行 (单选框) */
.option-row { 
  margin-bottom: 20px; 
  display: flex; 
  align-items: center; 
}

/* 选项标签文字 */
.label { 
  font-weight: bold; 
  margin-right: 15px; 
  color: #606266; 
  min-width: 80px;
}

/* 按钮区域 */
.action-area { 
  text-align: center; 
  margin-top: 40px; 
  padding-bottom: 10px;
}

/* 结果展示框 */
.result-box { 
  margin-top: 30px; 
  background: #f0f9eb; 
  padding: 20px; 
  border-radius: 6px; 
  border: 1px solid #e1f3d8;
  animation: fadeIn 0.5s; 
}

.result-box h4 {
  margin: 0 0 10px 0;
  color: #67c23a;
}

.result-content {
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap; /* 保持换行 */
  font-size: 15px;
}

.result-footer { 
  margin-top: 15px; 
  text-align: right; 
}

/* 简单的淡入动画 */
@keyframes fadeIn { 
  from { opacity: 0; transform: translateY(10px); } 
  to { opacity: 1; transform: translateY(0); } 
}
</style>