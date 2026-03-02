Page({
  data: {
    enter:true,
    username:'',
    password:'',
    register_tip:''
  },
 
//以下是监听输入框的数据并获取，和对登录按钮的设置：只有当输入框中都有数据时才能点击
  usernameInput:function(e){
    console.log(e)
    var val = e.detail.value;
      this.setData({
        username:val
      })
      if(val!='' && this.data.password!=''){
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
 
  passwordInput:function(e){
    var val = e.detail.value;
      this.setData({
        password:val
      })
      if(val!='' && this.data.username!=''){
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
    if(that.data.password.length>=12){
      that.setData({
        login_tip : "密码格式有误！"
      })
      return
    }
    wx.cloud.init({
      env:'ydwgbcqz-1ga7oe1gf698a328'
    })
    const db = wx.cloud.database()
    db.collection('user').where({
      username : that.data.username
    }).get({
      success: function(res) {
        console.log(res.data)
        if(res.data.length==0){
            db.collection('user').add({
              data:{
                username : that.data.username,
                password : that.data.password
              },
              success:function(res){
                that.setData({
                  register_tip : '注册成功！'
                })
                wx.navigateTo({
                  url: '/pages/login/login',
                })
              }
            })
        }
        else{
          that.setData({
            register_tip : '该用户已存在！'
          });
        }
      }
  })
}
})