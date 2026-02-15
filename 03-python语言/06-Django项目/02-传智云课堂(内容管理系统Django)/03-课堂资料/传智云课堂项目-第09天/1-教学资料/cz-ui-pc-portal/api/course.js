import http from './public'
import qs from 'qs'
let config = require('~/config/sysConfig')
let apiURL = config.apiURL
let staticURL = config.staticURL
if (typeof window === 'undefined') {
  apiURL = config.backApiURL
  staticURL = config.backStaticURL
}

