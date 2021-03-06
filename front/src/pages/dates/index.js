import Taro, { Component } from '@tarojs/taro'
import { View, Text} from '@tarojs/components'
import { connect } from '@tarojs/redux'
import moment from "moment"

import {request} from '../../utils/util';

import './index.less'

@connect(({ counter }) => ({
  counter
}))
export default class Index extends Component {
  config = {
    navigationBarTitleText: '日期',
    usingComponents: {
      "calendar": "plugin://calendar/calendar" 
    }
  }
  
  state = {
    times: [],
    dates: [],
    currentMonth: 0,
    currentYear: 0,
    dataMonth: 1
  }

  componentDidMount(){
    const {years, months} = moment().toObject();
    this.setState({
      dataMonth: months + 1,
      currentMonth: months + 1,
      currentYear: years
    }, this.fetchData);
  }

  fetchData = async () => {
    const {counter: {openId, info}} = this.props;
    const {cityName} = this.$router.params;
    const {currentMonth, currentYear} = this.state;
    Taro.showLoading({
      title: "加载中..."
    });
    try {
      const res = await request({
        url: `info/${cityName}`,
        data: {
          info_id: info[2],
          openId,
          search_year: currentYear,
          search_month: currentMonth
        },
        method: 'POST'
      });
      if(res.code === 200){
        let hasDate = res.data.length > 0;
        this.setState(Object.assign({
          dates: res.data,
        }, hasDate ? {
          dataMonth: res.data[0].split('/')[0],
          currentMonth: res.data[0].split('/')[0],
        }: {}));
      }
    } catch (error) {
      // pass
    }
    Taro.hideLoading();
  }

  getTimes = async () => {
    const {currentDay} = this.state;
    const {counter: {info, openId}} = this.props;
    const {cityName} = this.$router.params;
    const {years, months} = moment(currentDay, 'MM/DD/YYYY').toObject();
    Taro.showLoading({
      title: "加载中..."
    });
    const res = await request({
      url: `info/${cityName}`,
      data: {
        info_id: info[2],
        openId,
        search_year: years,
        search_month: months + 1,
        search_datetime: currentDay
      },
      method: 'POST'
    });
    if(res.code === 200){
      this.setState({
        times: res.data
      })
    }
    Taro.hideLoading();
  }

  dayClick = ({detail: {year, month, day}}) => {
    const formatedDate = moment([year, month - 1, day]).format('MM/DD/YYYY');
    const {dates=[]} = this.state;
    if(dates.find(d => d === formatedDate)){
      this.setState({
        currentDay: formatedDate
      }, this.getTimes);
    }
  }

  changeMonth = ({detail: {currentMonth, currentYear}}) => {
    const {dates} = this.state;
    // 如果有这个月的日期
    if(dates.find(day => {
      return +day.split('/')[0] === +currentMonth
    })){
      return ;
    }
    this.setState({
      currentMonth,
      dataMonth: currentMonth,
      currentYear
    }, this.fetchData);
  }

  render () {
    const {counter: { info }} = this.props;
    const {dates, currentMonth, currentYear, times, dataMonth} = this.state;
    const daysColor = (dates||[]).filter(d => {
      const [mon, , year] = d.split('/');
      return +mon === +currentMonth && +year === +currentYear
    }).map(day => {
      return {
        month: 'current',
        day: day.split('/')[1],
        color: '#fff',
        background: '#314580'
      }
    });
    return (
      <View className='container'>
        <View className='info' key={info[2]}>
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
        <View className='calendar'>
          <calendar  
            calendar-style='cal-calendar' 
            header-style='cal-header' 
            board-style='cal-board' 
            weeks-type='cn'
            month={dataMonth}
            days-color={daysColor}
            binddayClick='dayClick' 
            bindnextMonth='changeMonth' 
            bindprevMonth='changeMonth' 
            binddateChange='changeMonth' 
            ondayClick={this.dayClick.bind(this)}
            onNextMonth={this.changeMonth.bind(this)}
            onPrevMonth={this.changeMonth.bind(this)}
            onDateChange={this.changeMonth.bind(this)}
          />
        </View>
        {
          times.length > 0 ? (
            <View className='time-box'>
              {
                times.map(time => {
                  return (
                    <View key={time} className='time-item'>{time}</View>
                  )
                })
              }
            </View>
          ) : null
        }
      </View>
    )
  }
}