export type PaymentMethod = 'cash' | 'card'

export interface Trip {
  id: string
  start: string
  end: string
  amount: number
  payment: PaymentMethod
  commission: number
}

export interface DailySummary {
  trip_count: number
  revenue: number
  commission: number
  net_amount: number
  cash_amount: number
  card_amount: number
}

export interface DailyTrips {
  date: string
  trips: Trip[]
  summary: DailySummary
}
