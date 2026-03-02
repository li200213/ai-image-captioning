
Page({
  data: {
    history_list : wx.getStorageSync('history_list')
  },
  onShow(){
    this.setData({
      history_list : wx.getStorageSync('history_list')
    });
  }
})