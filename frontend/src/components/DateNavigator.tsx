import { formatDisplayDate, shiftDate } from '../utils/format'

interface DateNavigatorProps {
  selectedDate: string
  onDateChange: (date: string) => void
}

export function DateNavigator({ selectedDate, onDateChange }: DateNavigatorProps) {
  return (
    <section aria-label="Выбор даты" className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-medium text-slate-500">Выбранный день</p>
        <p className="mt-1 text-lg font-semibold text-slate-900">{formatDisplayDate(selectedDate)}</p>
      </div>
      <div className="grid grid-cols-[auto_minmax(0,1fr)_auto] items-center gap-2 sm:w-auto">
        <button
          type="button"
          onClick={() => onDateChange(shiftDate(selectedDate, -1))}
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-400 hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          aria-label="Предыдущий день"
        >
          ←
        </button>
        <label className="sr-only" htmlFor="selected-date">
          Выберите дату
        </label>
        <input
          id="selected-date"
          type="date"
          value={selectedDate}
          onChange={(event) => onDateChange(event.target.value)}
          className="min-w-0 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
        <button
          type="button"
          onClick={() => onDateChange(shiftDate(selectedDate, 1))}
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-400 hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          aria-label="Следующий день"
        >
          →
        </button>
      </div>
    </section>
  )
}
