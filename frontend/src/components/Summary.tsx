import type { DailySummary } from '../types/trips'
import { formatMoney } from '../utils/format'

interface SummaryProps {
  summary: DailySummary | null
  loading: boolean
}

const summaryItems = [
  { key: 'revenue', label: 'Выручка', emphasis: true },
  { key: 'commission', label: 'Комиссия', emphasis: false },
  { key: 'net_amount', label: 'На руки', emphasis: true },
  { key: 'trip_count', label: 'Поездок', emphasis: false },
] as const

export function Summary({ summary, loading }: SummaryProps) {
  return (
    <section aria-label="Сводка за день" className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {summaryItems.map((item) => (
        <article key={item.key} className="rounded-xl border border-slate-200 bg-white p-4">
          <p className="text-sm font-medium text-slate-500">{item.label}</p>
          {loading ? (
            <div className="mt-3 h-7 w-24 animate-pulse rounded bg-slate-100" />
          ) : (
            <p className={`mt-2 text-xl font-semibold ${item.emphasis ? 'text-slate-950' : 'text-slate-700'}`}>
              {item.key === 'trip_count' ? summary?.trip_count ?? 0 : formatMoney(summary?.[item.key] ?? 0)}
            </p>
          )}
        </article>
      ))}
    </section>
  )
}
