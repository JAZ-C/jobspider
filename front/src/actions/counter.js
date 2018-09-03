import Taro from '@tarojs/taro';
import {
  SHARE_SUCCESS,
  LOGIN
} from '../constants/const'
import {request, makeToast} from '../utils/util';

export const shareSuccess = () => {
  return {
    type: SHARE_SUCCESS
  }
}

export const login = ({userInfo}) => {
  return async dispatch => {
    // 调用小程序登录
    const loginData = await Taro.login();
    // 登录后, 用code换取openId
    const {code, message, data} = await request({
      url: 'login',
      data: {
        ...userInfo,
        code: loginData.code
      }
    });
    if(code !== 0){
      makeToast(message||'操作失败');
      return ;
    }
    // 更新openId
    dispatch({
      type: LOGIN,
      payload: data
    });
  }
}
