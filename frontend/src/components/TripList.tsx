import type { Trip } from '../types/trips'
import { formatMoney, formatTripTime } from '../utils/format'

interface TripListProps {
  trips: Trip[]
  loading: boolean
}

function paymentLabel(payment: Trip['payment']): string {
  return payment === 'cash' ? 'Наличные' : 'Карта'
}

export function TripList({ trips, loading }: TripListProps) {
  return (
    <section aria-labelledby="trips-heading" className="rounded-xl border border-slate-200 bg-white">
      <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
        <h2 id="trips-heading" className="text-base font-semibold text-slate-900">
          Поездки
        </h2>
        {!loading && <span className="text-sm text-slate-500">{trips.length}</span>}
      </div>

      {loading ? (
        <div className="space-y-3 p-5">
          {[1, 2, 3].map((item) => <div key={item} className="h-16 animate-pulse rounded-lg bg-slate-100" />)}
        </div>
      ) : trips.length === 0 ? (
        <div className="px-5 py-12 text-center">
          <p className="font-medium text-slate-700">Нет поездок за этот день</p>
          <p className="mt-1 text-sm text-slate-500">Выберите другую дату, чтобы посмотреть смену.</p>
        </div>
      ) : (
        <div className="divide-y divide-slate-100">
          <div className="hidden grid-cols-[1.2fr_1fr_1fr_1fr] gap-4 px-5 py-3 text-xs font-medium uppercase tracking-wide text-slate-500 sm:grid">
            <span>Время</span>
            <span>Сумма</span>
            <span>Комиссия</span>
            <span>Оплата</span>
          </div>
          {trips.map((trip) => (
            <article key={trip.id} className="grid grid-cols-2 gap-x-4 gap-y-3 px-5 py-4 sm:grid-cols-[1.2fr_1fr_1fr_1fr] sm:items-center">
              <div>
                <p className="text-xs font-medium text-slate-500 sm:hidden">Время</p>
                <p className="mt-1 font-medium text-slate-900 sm:mt-0">{formatTripTime(trip.start)}–{formatTripTime(trip.end)}</p>
              </div>
              <div>
                <p className="text-xs font-medium text-slate-500 sm:hidden">Сумма</p>
                <p className="mt-1 font-medium text-slate-900 sm:mt-0">{formatMoney(trip.amount)}</p>
              </div>
              <div>
                <p className="text-xs font-medium text-slate-500 sm:hidden">Комиссия</p>
                <p className="mt-1 text-slate-700 sm:mt-0">{formatMoney(trip.commission)}</p>
              </div>
              <div>
                <p className="text-xs font-medium text-slate-500 sm:hidden">Оплата</p>
                <span className={`mt-1 inline-flex rounded-full px-2.5 py-1 text-xs font-medium sm:mt-0 ${trip.payment === 'cash' ? 'bg-emerald-50 text-emerald-800' : 'bg-blue-50 text-blue-800'}`}>
                  {paymentLabel(trip.payment)}
                </span>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}
