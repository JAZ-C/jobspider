import Taro, { Component } from '@tarojs/taro'
import { View, Button, Text, Image, Input } from '@tarojs/components'
import { connect } from '@tarojs/redux'

import { login, updateShareNum } from '../../actions/counter'
import {baseUrl, makeToast} from '../../utils/util';
import AuthModal from '../../components/auth-modal/auth-modal';

import './index.less'

@connect(({ counter }) => ({
  counter
}), (dispatch) => ({
  login (userInfo) {
    dispatch(login(userInfo))
  },
  updateShareNum (openId) {
    dispatch(updateShareNum(openId))
  },
}))
export default class Index extends Component {
  config = {
    navigationBarTitleText: '首页'
  }

  state = {
    showGetUserInfoModal: false, // 获取用户信息弹窗
    showInfoImg: false, //分享二维码
    cityName: ''
  }

  componentDidMount(){
    this.getUserInfo();
    Taro.showLoading();
  }

  componentWillReceiveProps({counter: openId}){
    if(openId){
      Taro.hideLoading();
    }
  }

  /**
   * 获取用户信息
   */
  getUserInfo = async (info) => {
    if(info){
      // 这是已经获取到userInfo的情况(第一次登陆, 授权)
      Taro.showLoading();
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
      }, () => {
        Taro.hideLoading();
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
    this.updateShareNum(this.props.counter.openId);
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

  getInputText = (e) => {
    this.setState({
      cityName: e.detail.value
    });
  }

  search = () => {
    const {cityName} = this.state;
    const {counter: {shareNum}} = this.props;
    if(!cityName){
      makeToast('请输入城市名称.');
      return ;
    }
    if(shareNum === 0){
      makeToast('转发后才可使用哦.');
      return ;
    }
    Taro.navigateTo({
      url: '/pages/list/index?searchText=' + cityName
    });
  }

  render () {
    const {showGetUserInfoModal, showInfoImg, cityName} = this.state;
    return (
      <View className='container'>
        <View className='container-top-btns'>
          <Button className='ctrl-btn' open-type='share'>
            <Text className='iconfont icon-xingqiu'></Text>
            <Text>转发可免费查询</Text>
          </Button>
          <View className='divi-line'></View>
          <Button className='ctrl-btn' onClick={this.showInfoImg.bind(this)}>
            <Text className='iconfont icon-qunzu'></Text>
            <Text>加入考位分享群</Text>
          </Button>
        </View>
        <View className='tips'>转发到群里即可免费查询</View>
        <View className='container-top-search'>
          <Input className='search-input' placeholder='输入城市...' value={cityName} onInput={this.getInputText} />
          <Button onClick={this.search} className='search-btn'>查询</Button>
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