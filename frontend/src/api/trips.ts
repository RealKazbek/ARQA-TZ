import type { DailyTrips } from '../types/trips'

const apiUrl = import.meta.env.VITE_API_URL?.replace(/\/$/, '') ?? ''

export class TripsApiError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'TripsApiError'
  }
}

export async function getDailyTrips(date: string): Promise<DailyTrips> {
  let response: Response

  try {
    response = await fetch(`${apiUrl}/api/trips?date=${encodeURIComponent(date)}`)
  } catch {
    throw new TripsApiError('Не удалось подключиться к серверу. Попробуйте ещё раз.')
  }

  if (!response.ok) {
    throw new TripsApiError('Не удалось загрузить данные за выбранный день.')
  }

  return response.json()
}
