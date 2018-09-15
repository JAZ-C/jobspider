import Taro from '@tarojs/taro';

// export const baseUrl = "https://www.28ty.cn/";
export const baseUrl = "http://192.168.199.159:5000/";

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
    }
    console.log(res);
    return res.data;
  } catch (error) {
    makeToast('请求超时');
    return {};
  }
}