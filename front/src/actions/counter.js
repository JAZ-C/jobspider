import Taro from '@tarojs/taro';
import {
  LOGIN,
  UPDATE_SHARE_NUM,
  SET_INFO
} from '../constants/const'
import {request, makeToast} from '../utils/util';

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
      payload: data.openId
    });
    dispatch({
      type: UPDATE_SHARE_NUM,
      payload: data.shareNum
    })
  }
}

export const updateShareNum = openId => {
  return async dispatch => {
    const {code} = await request({
      url: 'update_share_num',
      method: "GET",
      data: {
        openId
      }
    });
    if(code === 0){
      dispatch({
        type: UPDATE_SHARE_NUM
      })
    }
  }
}

export const setInfo = info => {
  return dispatch => {
    dispatch({
      type: SET_INFO,
      payload: info
    })
  }
}