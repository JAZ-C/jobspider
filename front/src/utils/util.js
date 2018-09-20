import Taro from '@tarojs/taro';

export const baseUrl = "https://www.aciaus.com/";
// export const baseUrl = "http://192.168.199.159:5000/";

export const makeToast = title => {
  return Taro.showToast({
    title,
    icon: 'none'
  });
}

export const request = async ({url, data, method="POST"}) => {
  try {
    const res = await Taro.request({
      url: baseUrl + url,
      method,
      data
    });
    if(res.statusCode === 200){
      return res.data;
    }else{
      Taro.showModal({
        title: '提示',
        content: '数据加载失败, 请稍后重试.'
      });
      return {};
    }
  } catch (error) {
    Taro.showModal({
      title: '提示',
      content: '请求超时, 请稍后重试.'
    });
    return {};
  }
}