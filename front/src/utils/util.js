import Taro from '@tarojs/taro';

export const baseUrl = "http://192.168.199.159:5000/";

export const makeToast = title => {
  return Taro.showToast({
    title,
    icon: 'none'
  });
}

export const request = async ({url, data, method="POST"}) => {
  const res = await Taro.request({
    url: baseUrl + url,
    method,
    data
  });
  console.log(res);
  if(res.statusCode === 200){
    return res.data;
  }
  return res.data;
}