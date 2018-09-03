import { SHARE_SUCCESS, LOGIN } from '../constants/const'

const INITIAL_STATE = {
  shareNum: 0,
  openId: null
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case SHARE_SUCCESS:
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
