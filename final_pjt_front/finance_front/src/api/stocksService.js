import { format, subDays, subWeeks, subMonths } from 'date-fns'
import { createExternalApi } from './externalApi'
import { externalConfig } from './config'

const stocksService = createExternalApi(externalConfig.stocks)

export function fetchData(endpoint, params) {
  return stocksService.get(endpoint, { params })
}

export function getStocksList(rest) {
  const params = {
    serviceKey: import.meta.env.VITE_STOCK_DECODED_API_KEY,
    resultType: 'json',
    ...rest,
  }
  console.log(params)
  console.log(rest)
  return fetchData('/getStockPriceInfo', params)
}

/**
 * 주식 시세 조회 (단위별)
 * @param {object} options
 * @param {'daily'|'weekly'|'monthly'} options.unit 조회 단위
 * @param {number} options.count 조회 개수 (일/주/월 개수)
 * @param {object} options.rest 추가 필터 파라미터 (itmsNm, isinCd 등)
 */

export function getPriceByUnit({ unit = 'daily', count = 30, ...rest }) {
  const today = new Date()
  let beginDate
  // console.log('today: ', today)
  // console.log('unit: ', unit)

  if (unit === 'daily') {
    beginDate = subDays(today, 1) // 1일 전
  } else if (unit === 'weekly') {
    beginDate = subWeeks(today, 1) // 1주 전
  } else if (unit === 'monthly') {
    beginDate = subMonths(today, 1) // 1달 전
  }
  // console.log('beginDate: ', beginDate)
  const beginBasDt = format(beginDate, 'yyyyMMdd')
  const endBasDt = format(today, 'yyyyMMdd')

  // console.log('beginBasDt: ', beginBasDt)
  // console.log('endBasDt: ', endBasDt)

  const params = {
    serviceKey: import.meta.env.VITE_STOCK_DECODED_API_KEY,
    numOfRows: count,
    pageNo: 1,
    resultType: 'json',
    beginBasDt,
    endBasDt,
    ...rest,
  }
  console.log('HIEE')
  return fetchData('/getStockPriceInfo', params)
}
