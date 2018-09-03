import Taro from '@tarojs/taro';

export const baseUrl = "http://localhost:5000/";

export const makeToast = title => {
  return Taro.showToast({
    title,
    icon: 'none'
  });
}

export const request = async ({url, data, method="post", header={}}) => {
  const res = await Taro.request({
    url: baseUrl + url,
    method,
    data,
    header
  });
  if(res.statusCode === 200){
    return res.data;
  }
  return res.data;
}