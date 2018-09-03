import Taro, { Component } from '@tarojs/taro'
import { View, Button, Text, Image } from '@tarojs/components'
import { connect } from '@tarojs/redux'

import { shareSuccess, login } from '../../actions/counter'
import {baseUrl} from '../../utils/util';
import AuthModal from '../../components/auth-modal/auth-modal';

import './index.less'

@connect(({ counter }) => ({
  counter
}), (dispatch) => ({
  shareSuccess () {
    dispatch(shareSuccess())
  },
  login (userInfo) {
    dispatch(login(userInfo))
  }
}))
export default class Index extends Component {
  config = {
    navigationBarTitleText: '首页'
  }

  state = {
    showGetUserInfoModal: false, // 获取用户信息弹窗
    showInfoImg: false, //分享二维码
  }

  componentDidMount(){
    this.getUserInfo();
  }

  /**
   * 获取用户信息
   */
  getUserInfo = async (info) => {
    if(info){
      // 这是已经获取到userInfo的情况
      this.setState({
        showGetUserInfoModal: false
      }, () => this.login(info));
      return ;
    }
    try {
      const setting = await Taro.getSetting();
      if (!setting.authSetting['scope.userInfo']){
        throw new Error('获取用户信息失败');
      }
      const userInfo = await Taro.getUserInfo();
      if(!userInfo){
        throw new Error('获取用户信息失败');
      }
      this.login(userInfo);
    } catch (error) {
      this.setState({
        showGetUserInfoModal: true
      });
    }
  }

  /**
   * 分享
   */
  onShareAppMessage = () => {
    Taro.showShareMenu({
      withShareTicket: true
    });
    return {
      title: '雅思小程序',
      success: this.shareSuccess,
      fail: this.cancelShare
    }
  }

  /**
   * 转发成功
   */
  shareSuccess = () => {
    Taro.showToast({
      title: '转发成功',
      icon: 'none'
    });
    this.shareSuccess();
  }

  /**
   * 取消转发
   */
  cancelShare = () => {
    Taro.showToast({
      title: '转发后才能正常使用哦',
      icon: 'none'
    });
  }

  /**
   * 显示分享二维码
   */
  showInfoImg = () => {
    this.setState({
      showInfoImg: true,
    });
  }

  /**
   * 隐藏分享二维码
   */
  hideInfoImg = () => {
    this.setState({
      showInfoImg: false
    })
  }

  render () {
    const {showGetUserInfoModal, showInfoImg} = this.state;
    return (
      <View className='container'>
        <View className='container-top'>
          <Button className='forward' open-type='share'>转发</Button>
          <Button className='forward' onClick={this.showInfoImg.bind(this)}>加入考位分享群</Button>
          <Button className='forward'>转发</Button>
          <Text>转发小程序到群即可免费查询</Text>
        </View>
        {/* 获取授权弹窗 */}
        {
          showGetUserInfoModal ? (
            <AuthModal 
              showCancelBtn={false}
              // onCancel={this.cancelGetUserInfo.bind(this)} 
              onOk={this.getUserInfo.bind(this)} 
            />
          ) : null
        }
        {
          showInfoImg ? (
            <View className='share-img-container'>
              <View className='share-img-content'>
                <Text className='info-img-title'>扫描下方二维码</Text>
                <Image className='info-img' src={baseUrl + 'static/info-img.jpeg'}></Image>
                <Button className='hide-info-img' onClick={this.hideInfoImg.bind(this)}>我知道了</Button>
              </View>
            </View>
          ) : null
        }
      </View>
    )
  }
}