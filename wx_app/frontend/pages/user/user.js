// pages/user/user.js
Page({
  data: {
    isHidden : true,
    enter:true,
    username : wx.getStorageSync('username'),
    password : wx.getStorageSync('password'),
    new_password : '',
    update_tip:''
  },

  onShow: function () {
    // 每次页面加载时重新初始化data
    this.setData({
      isHidden : true,
      update_tip:''
    });
  },
  toggleHidden() {
    this.setData({
      isHidden: !this.data.isHidden
    });
  },
  new_passwordInput:function(e){
    var val = e.detail.value;
      this.setData({
        new_password:val
      })
      if(val!=''){
        this.setData({
          enter:false
        })
      }
      else{
        this.setData({
          enter:true
        })
      }
  },
  post:function(){
    var that = this;
    if(that.data.password==that.data.new_password){
      that.setData({
        update_tip : '与原密码相同，修改无效'
      })
    }
    wx.cloud.init({
        env:'ydwgbcqz-1ga7oe1gf698a328'
    })
    const db = wx.cloud.database()
    db.collection("user").where({
      username:that.data.username
    }).update({
      data:{
        password:that.data.new_password
      }
    }).then(res=>{
      console.log(res)
      that.setData({
        update_tip : '修改成功！',
        password : that.data.new_password
      })
    })
  }
           
})