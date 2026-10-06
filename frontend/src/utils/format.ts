export function formatMoney(amount: number): string {
  const formatted = new Intl.NumberFormat('ru-RU', {
    maximumFractionDigits: 0,
  })
    .format(amount)
    .replace(/\u00a0/g, ' ')

  return `${formatted} ₸`
}

export function formatDisplayDate(value: string): string {
  const [year, month, day] = value.split('-').map(Number)
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(year, month - 1, day, 12))
}

export function shiftDate(value: string, offset: number): string {
  const [year, month, day] = value.split('-').map(Number)
  const nextDate = new Date(year, month - 1, day + offset, 12)
  const nextMonth = String(nextDate.getMonth() + 1).padStart(2, '0')
  const nextDay = String(nextDate.getDate()).padStart(2, '0')

  return `${nextDate.getFullYear()}-${nextMonth}-${nextDay}`
}

export function formatTripTime(timestamp: string): string {
  return timestamp.slice(11, 16)
}
