import Taro, { Component } from '@tarojs/taro'
import { View, Text} from '@tarojs/components'
import { connect } from '@tarojs/redux'

import {request} from '../../utils/util';
import { setInfo } from '../../actions/counter'

import './index.less'

@connect(({ counter }) => ({
  counter
}), dispatch => (
  {
    setInfo(info){
      dispatch(setInfo(info))
    }
  }
))
export default class Index extends Component {
  config = {
    navigationBarTitleText: '考位列表',
  }

  state = {
    firstLoad: true,
    cityName: '',
    infoList: []
  }

  componentDidMount(){
    this.setState({
      cityName: this.$router.params.searchText
    }, this.fetchData(this.$router.params.searchText));
  }

  fetchData = async cityName => {
    Taro.showLoading({
      title: "加载中..."
    });
    let city = cityName || this.state.cityName;
    const {counter: {openId}} = this.props;
    const res = await request({
      url: `info/${city}?openId=${openId}`,
      method: 'GET'
    });
    if(res.code === 200){
      this.setState({
        firstLoad: false,
        infoList: res[cityName]
      });
    }
    setTimeout(() => {
      Taro.hideLoading();
    }, 1000);
  }

  getDetail = (info, cityName) => {
    this.setInfo(info);
    Taro.navigateTo({
      url: '/pages/dates/index?cityName=' + cityName
    })
  }

  render () {
    const {infoList, cityName, firstLoad} = this.state;
    return (
      <View className='container'>
        {
          (infoList.length === 0 && !firstLoad) ? (
            <View className='no-data'>没有数据.</View>
          ) : null
        }
        {
          (infoList.length > 0) ? infoList.map(info => {
            console.log(info[0].toUpperCase());
            return info[0].toUpperCase().indexOf(cityName.toUpperCase()) > -1 ? (
              <View 
                className='info' 
                key={info[2]} 
                onClick={this.getDetail.bind(this, info, cityName)}
              >
                <View className='info-tc_name'>
                  <Text>{info[0]}</Text>
                </View>
                <View className='info-tc_address'>
                  {
                    info[1].map(addr => {
                      return (
                        <Text className='addr-item' key={addr}>{addr}</Text>
                      )
                    })
                  }
                </View>
              </View>
            ) : null
          }) : null
        }
      </View>
    )
  }
}