import Taro, { Component } from '@tarojs/taro'
import { View, Text} from '@tarojs/components'
import { connect } from '@tarojs/redux'

import {request} from '../../utils/util';

import './index.less'

@connect(({ counter }) => ({
  counter
}))
export default class Index extends Component {
  config = {
    navigationBarTitleText: '考位详情'
  }
  
  state = {
    tc_info: [],
  }

  componentDidMount(){
    const {counter: {info}} = this.props;
    const cityName = this.$router.params.cityName;
    this.fetchData(info, cityName);
  }

  fetchData = async ([, , info_id, url], cityName) => {
    Taro.showLoading({
      title: "加载中..."
    });
    const {counter: {openId}} = this.props;
    const res = await request({
      url: `info/${cityName}`,
      data: {
        info_id,
        url,
        openId
      },
      method: 'POST'
    });
    if(res.code === 200){
      this.setState({
        tc_info: res.tc_info
      });
    }
    console.log(res)
    Taro.hideLoading();
  }

  render () {
    const {counter: { info }} = this.props;
    const {tc_info} = this.state;
    return (
      <View className='container'>
        <View className='tc_name'>{tc_info[0]}</View>
        <View className='tc_phone'>{tc_info[1]}</View>
        <View className='tc_address'>
          {
            (tc_info.length > 0 ? info[1] : []).map(addr => {
              return (
                <Text key={addr} className='addr-item'>{addr}</Text>
              )
            })
          }
        </View>
        <View className='tc_dir'>
          {tc_info[2]}
        </View>
      </View>
    )
  }
}