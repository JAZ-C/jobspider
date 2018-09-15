import Taro, { Component } from '@tarojs/taro'
import '@tarojs/async-await'
import { Provider } from '@tarojs/redux'

import Index from './pages/index'

import configStore from './store'

import './app.less'

const store = configStore()

class App extends Component {
  config = {
    pages: [
      'pages/index/index',
      'pages/list/index',
      'pages/detail/index',
      'pages/dates/index',
    ],
    window: {
      backgroundTextStyle: 'light',
      navigationBarBackgroundColor: '#fff',
      navigationBarTitleText: 'WeChat',
      navigationBarTextStyle: 'black'
    },
    plugins: {
      calendar: {
          version: "1.1.3",
          provider: "wx92c68dae5a8bb046"
      }
    }
  }

  render () {
    return (
      <Provider store={store}>
        <Index />
      </Provider>
    )
  }
}

Taro.render(<App />, document.getElementById('app'))
