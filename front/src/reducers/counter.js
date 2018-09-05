import { LOGIN, UPDATE_SHARE_NUM } from '../constants/const'

const INITIAL_STATE = {
  shareNum: 0,
  openId: null
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case UPDATE_SHARE_NUM:
      return {
        ...state,
        shareNum: state.shareNum + 1
      }
     case LOGIN:
       return {
         ...state,
         openId: action.payload
       }
     default:
       return state
  }
}
