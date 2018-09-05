import Taro, { Component } from '@tarojs/taro'
import { View, Button } from '@tarojs/components'

import "./auth-modal.less"

export default class AuthModal extends Component{

  /**
   * 点击确定授权
   */
  handleOk = ({detail}) => {
    const {onOk} = this.props;
    onOk && onOk(detail);
  }

  /**
   * 点击取消
   */
  handleCancel = () => {
    const {onCancel} = this.props;
    onCancel && onCancel();
  }

  render(){
    const {showCancelBtn} = this.props;
    return (
      <View className='auth-modal'>
        <View className='auth-content'>
          <View className='auth-title'>微信授权</View>
          <View className='auth-detail'>
            <View className='auth-tips'>获得您的公开信息(头像, 昵称等)</View>
          </View>
          <View className='auth-btns'>
            {
              showCancelBtn && <Button className='auth-btn confirm-btn' openType='getUserInfo' onGetUserInfo={this.handleOk}>授权</Button>
            }
            <Button className='auth-btn confirm-btn' openType='getUserInfo' onGetUserInfo={this.handleOk}>授权</Button>
          </View>
        </View>
      </View>
    )
  }
}