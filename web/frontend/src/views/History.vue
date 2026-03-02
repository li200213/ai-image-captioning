<template>
  <div style="padding: 20px;">
    
    <!-- ================== 1. 顶部导航栏 ================== -->
    <div class="header">
      <!-- 左侧：系统标题 (点击可回首页) -->
      <div class="logo" @click="goHome">
        智能看图配文系统
      </div>

      <!-- 右侧：用户信息 -->
      <div class="user-area">
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">
            <el-avatar :size="32" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <span class="username">{{ username }}</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="home" :icon="House">返回首页</el-dropdown-item>
              <el-dropdown-item command="logout" :icon="SwitchButton" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- ================== 2. 历史记录表格 ================== -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <div style="font-weight: bold;">📜 历史生成记录</div>
      </template>
      
      <el-table :data="tableData" style="width: 100%" border stripe v-loading="loading">
        
        <!-- 列1：时间 -->
        <el-table-column prop="time" label="时间" width="180" align="center" sortable />
        
        <!-- 列2：图片预览 (核心修改部分) -->
        <el-table-column label="图片预览 (点击放大)" width="240" header-align="center">
          <template #default="scope">
            <div class="nine-grid-layout">
              <!-- 
                preview-src-list: 指定点击放大后的大图列表
                initial-index: 指定点击时从第几张开始展示
                preview-teleported: 必须加！防止弹窗被表格遮住
               -->
              <el-image 
                v-for="(url, index) in scope.row.imgList"
                :key="index"
                :src="url"
                :preview-src-list="scope.row.imgList" 
                :initial-index="index"
                fit="cover" 
                class="grid-img"
                preview-teleported
                hide-on-click-modal
              />
            </div>
            <div v-if="scope.row.imgList.length === 0" style="color:#999;font-size:12px;text-align:center;">
              无图片
            </div>
          </template>
        </el-table-column>

        <!-- 列3：风格 -->
        <el-table-column label="配文风格" width="120" align="center">
          <template #default="scope">
            <el-tag effect="plain">{{ scope.row.style }}</el-tag>
          </template>
        </el-table-column>

        <!-- 列4：情绪 -->
        <el-table-column label="情绪色彩" width="120" align="center">
          <template #default="scope">
            <el-tag :type="getEmotionColor(scope.row.emotion)" effect="dark">
              {{ scope.row.emotion }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 列5：配文结果 -->
        <el-table-column prop="caption" label="生成的配文" min-width="300" header-align="center" align="left">
          <template #default="scope">
            <div class="caption-text">{{ scope.row.caption }}</div>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router' // 👈 必须引入这个
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ArrowDown, SwitchButton, House } from '@element-plus/icons-vue'

const router = useRouter() // 👈 必须初始化
const tableData = ref([])
const loading = ref(false)
const username = ref('未登录') // 👈 定义成响应式变量

// 辅助函数：颜色映射
const getEmotionColor = (emotion) => {
  const map = {
    '开心': 'success', 
    '忧伤': 'info',   
    '平静': '',       
  }
  return map[emotion] || ''
}

// 导航逻辑
const goHome = () => router.push('/home')

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('username')
    router.push('/login')
    ElMessage.success('已退出登录')
  } else if (command === 'home') {
    router.push('/home')
  }
}

// 初始化数据
onMounted(async () => {
  loading.value = true
  const storedName = localStorage.getItem('username')
  if (storedName) {
    username.value = storedName
  }

  try {
    const response = await axios.get('http://127.0.0.1:5000/api/history', {
      params: { username: username.value }
    })
    
    if (response.data.code === 200) {
      const rawData = response.data.data
      
      tableData.value = rawData.map(item => {
        // 图片路径处理
        const pathStr = item.img_src || ''
        
        // 1. 分割字符串
        // 2. 替换反斜杠 \ 为正斜杠 /
        // 3. 拼接完整的服务器地址
        const imgUrls = pathStr.split(';')
          .filter(path => path && path.trim() !== '')
          .map(path => `http://127.0.0.1:5000/${path.replace(/\\/g, '/')}`)

        return {
          time: item.time,  
          imgList: imgUrls,        
          style: item.text_type,   
          emotion: item.emotion, 
          caption: item.caption 
        }
      })
      
      // 按时间倒序（最新的在上面）
      tableData.value.reverse()
    }
  } catch (error) {
    console.error('获取历史记录失败', error)
    ElMessage.error('无法连接服务器')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
@import '../assets/header.css';

/* 1. 图片容器：去除高度限制，允许自动撑开 */
.nine-grid-layout {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 8px;        /* 图片之间的间距 */
  width: 100%;     
  /* 👇 删掉了 max-height 和 overflow-y */
  padding: 4px 0;
}

/* 2. 单张小图样式 */
.grid-img {
  width: 60px;     /* 图片宽度 */
  height: 60px;    /* 图片高度 */
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  object-fit: cover;
  cursor: zoom-in;
}

/* 3. 文字容器：去除高度限制，允许自动撑开 */
.caption-text {
  white-space: pre-wrap; 
  line-height: 1.6;
  font-size: 14px;
  color: #333;
  padding: 5px 0;
}


:deep(.el-table__body .el-table__cell) {
  vertical-align: top !important;
}

:deep(.el-table .cell) {
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>