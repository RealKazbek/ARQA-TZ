import { useEffect, useState } from 'react'
import { getDailyTrips } from './api/trips'
import { DateNavigator } from './components/DateNavigator'
import { PaymentBreakdown } from './components/PaymentBreakdown'
import { Summary } from './components/Summary'
import { TripList } from './components/TripList'
import type { DailyTrips } from './types/trips'

const INITIAL_DATE = '2026-10-01'

export default function App() {
  const [selectedDate, setSelectedDate] = useState(INITIAL_DATE)
  const [dailyTrips, setDailyTrips] = useState<DailyTrips | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [retryKey, setRetryKey] = useState(0)

  useEffect(() => {
    let active = true

    async function loadTrips() {
      setLoading(true)
      setError('')
      setDailyTrips(null)

      try {
        const response = await getDailyTrips(selectedDate)
        if (active) {
          setDailyTrips(response)
        }
      } catch (loadError) {
        if (active) {
          setError(loadError instanceof Error ? loadError.message : 'Не удалось загрузить данные.')
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    void loadTrips()

    return () => {
      active = false
    }
  }, [selectedDate, retryKey])

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:py-12">
      <div className="mx-auto max-w-5xl space-y-6">
        <header>
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-blue-700">Смена водителя</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Дневник смен</h1>
          <p className="mt-2 text-slate-600">Поездки и финансовый итог за выбранный день.</p>
        </header>

        <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
          <DateNavigator selectedDate={selectedDate} onDateChange={setSelectedDate} />
        </div>

        {error && (
          <section role="alert" className="flex flex-col gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 sm:flex-row sm:items-center sm:justify-between">
            <p>{error}</p>
            <button
              type="button"
              onClick={() => setRetryKey((key) => key + 1)}
              className="self-start rounded-lg border border-red-300 bg-white px-3 py-2 font-medium text-red-800 hover:bg-red-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-700 sm:self-auto"
            >
              Повторить
            </button>
          </section>
        )}

        <Summary summary={dailyTrips?.summary ?? null} loading={loading} />
        <PaymentBreakdown summary={dailyTrips?.summary ?? null} loading={loading} />
        <TripList trips={dailyTrips?.trips ?? []} loading={loading} />
      </div>
    </main>
  )
}
