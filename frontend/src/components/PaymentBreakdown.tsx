import type { DailySummary } from '../types/trips'
import { formatMoney } from '../utils/format'

interface PaymentBreakdownProps {
  summary: DailySummary | null
  loading: boolean
}

export function PaymentBreakdown({ summary, loading }: PaymentBreakdownProps) {
  return (
    <section aria-labelledby="payment-heading" className="rounded-xl border border-slate-200 bg-white p-5">
      <h2 id="payment-heading" className="text-base font-semibold text-slate-900">
        Способ оплаты
      </h2>
      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-lg bg-emerald-50 p-4">
          <p className="text-sm font-medium text-emerald-800">Наличные</p>
          {loading ? <div className="mt-3 h-6 w-20 animate-pulse rounded bg-emerald-100" /> : <p className="mt-2 text-lg font-semibold text-emerald-950">{formatMoney(summary?.cash_amount ?? 0)}</p>}
        </div>
        <div className="rounded-lg bg-blue-50 p-4">
          <p className="text-sm font-medium text-blue-800">Карта</p>
          {loading ? <div className="mt-3 h-6 w-20 animate-pulse rounded bg-blue-100" /> : <p className="mt-2 text-lg font-semibold text-blue-950">{formatMoney(summary?.card_amount ?? 0)}</p>}
        </div>
      </div>
    </section>
  )
}
