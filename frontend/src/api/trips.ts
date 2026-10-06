import type { DailyTrips } from '../types/trips'

export class TripsApiError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'TripsApiError'
  }
}

export async function getDailyTrips(date: string): Promise<DailyTrips> {
  let response: Response

  try {
    response = await fetch(`/api/trips?date=${encodeURIComponent(date)}`)
  } catch {
    throw new TripsApiError('Не удалось подключиться к серверу. Попробуйте ещё раз.')
  }

  if (!response.ok) {
    throw new TripsApiError('Не удалось загрузить данные за выбранный день.')
  }

  return response.json()
}
