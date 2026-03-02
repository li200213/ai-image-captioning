Page({
  data:{
    imageSrcs : [],
    img_base64 : [],
    weixin_txt:'',
    text_type_list : ["朋友圈配文","七言绝句","五言绝句","诗歌","小作文","吐槽"],
    text_type_index : 0,
    text_type : "朋友圈配文",
    emotion_list : ["无","开心的","忧郁的","孤独的","疲惫的","伤心的","亢奋的"],
    emotion_index : 0,
    emotion : "无"
  },

  chooseImage() {
    var that = this
    wx.chooseMedia({
      count: 4, // 可选择的图片数量
      sizeType : ['original','compressed'],
      sourceType: ['album', 'camera'],
      success:  (res)=> {
        console.log(res.tempFiles)
        var tempFilePaths = []
        for(var i = 0; i < res.tempFiles.length; i++){
          tempFilePaths.push(res.tempFiles[i].tempFilePath)
        }
        that.setData({
          imageSrcs : tempFilePaths
        })
   
        }
      })
  },
 
  call_api(){
    var that = this
    if(that.data.imageSrcs.length==0){
      return wx.showToast({
        title: '请先上传图片',
        icon : 'error'
      })
    }
    wx.showLoading({
      title: 'Loading...',
    })
    
    var tempFilePaths = this.data.imageSrcs
    //上传数据到云存储
    wx.cloud.init({
      "env": "ydwgbcqz-1ga7oe1gf698a328"
    })
    // var base64 = [],
    var fileIDs = '';
    for (var i = 0; i < tempFilePaths.length; i++) {
        var imgSrc = tempFilePaths[i];
        wx.cloud.uploadFile({
          cloudPath: imgSrc.split('/')[imgSrc.split('/').length-1],
          filePath: imgSrc,
          success: function (res) {
            console.log(res)
            fileIDs=fileIDs+res.fileID+";"
          },
          fail: function (res) {
            console.log("error");
          }
        })
        // //图片base64编码，方便后续request提交到后端
        // wx.getFileSystemManager().readFile({
        //   filePath: imgSrc,
        //   encoding: 'base64',
        //   success: function (res) {
        //     base64.push(res.data)
        //   }
        // });
        
        // that.setData({
        //   img_base64 : base64
        // })
      }
      
      setTimeout(function(){
          // wx.request({
          //   url: 'https://..../call_api',
          //   header: {
          //     'content-type': 'application/x-www-form-urlencoded',
          //     'chartset': 'utf-8'
          //   },
          //   data: {
          //     username : JSON.stringify(wx.getStorageSync('username')),
          //     img_base64 : JSON.stringify(that.data.img_base64),
          //     text_type : JSON.stringify(that.data.text_type),
          //     emotion : JSON.stringify(that.data.emotion)
          //   },
          //   method: 'POST',
          //   success: function(res) {
          //     that.setData({
          //       weixin_txt : res.data['result']
          //     })
          //     db.collection('history').add({
          //       data:{
          //         username : wx.getStorageSync('username'),
          //         time : res.data['result_time'], 
          //         img_src : that.data.fileIDs,
          //         text_type : that.data.text_type,
          //         emotion : that.data.emotion,
          //         text : that.data.weixin_txt
          //       },
          //       success:function(res){
          //         console.log("success")
          //       }
          //      })
          //   },
          //   fail: function(f) {
          //     console.log(f)
          //   },
          // })
        setTimeout(function() {
          var result_time = new Date().toJSON().substring(0, 10) + ' ' + new Date().toTimeString().substring(0,8)
          wx.hideLoading()
          that.setData({
            weixin_txt : "舟行水道间，楼影映波澜。佳人高楼立，夕阳乐心田。"
          })
          wx.cloud.init({
            env:'ydwgbcqz-1ga7oe1gf698a328'
          })
          const db = wx.cloud.database()
          db.collection('history').add({
            data:{
              username : wx.getStorageSync('username'),
              time : result_time,
              img_src : fileIDs,
              text_type : that.data.text_type,
              emotion : that.data.emotion,
              text : that.data.weixin_txt
            },
            success:function(res){
              console.log("success")

              //刷新历史记录
                db.collection('history').where({
                  username : wx.getStorageSync('username')
                }).get({
                success: function(res) {
                  console.log(res.data)
                  wx.setStorageSync('history_list', res.data);
                }
              })
            }
          })
          }, 150000);
        },3000);
  },
  text_type(e){
    this.setData({
      text_type_index: e.detail.value,
      text_type : this.data.text_type_list[e.detail.value]
    })
  },
  emotion(e){
    var emotion = e.detail.value;
    this.setData({
      emotion_index: e.detail.value,
      emotion : this.data.emotion_list[e.detail.value]
    })
  },

  //预览图片
  PreviewImg: function (e) {
    var that = this;
    var index = e.target.dataset.index; //获取所有显示图片的下标

    wx.previewImage({
      current: that.data.imageSrcs[index],
      urls: that.data.imageSrcs,
    })
  },

  //长按删除图片
  DeleteImg: function (e) {
    var that = this;
    var tempFilePaths = that.data.imageSrcs;
    var index = e.currentTarget.dataset.index;//获取当前长按图片下标

    wx.showModal({
      title: '提示',
      content: '确定要删除此图片吗？',
      success: function (res) {
        if (res.confirm) {
          tempFilePaths.splice(index, 1);
        } else if (res.cancel) {
          return false;
        }
        that.setData({
          imageSrcs : tempFilePaths
        });

      }

    })

  },
})

