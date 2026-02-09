"use client";

const patterns = [
  { value: "", label: "None" },
  { value: "daily", label: "Daily" },
  { value: "weekly", label: "Weekly" },
  { value: "monthly", label: "Monthly" },
  { value: "yearly", label: "Yearly" },
] as const;

interface RecurrenceSelectorProps {
  pattern: string;
  endDate: string;
  onPatternChange: (pattern: string) => void;
  onEndDateChange: (date: string) => void;
}

export default function RecurrenceSelector({
  pattern,
  endDate,
  onPatternChange,
  onEndDateChange,
}: RecurrenceSelectorProps) {
  return (
    <div className="space-y-2">
      <label className="block text-xs font-medium text-gray-400 uppercase tracking-wider">
        Repeat
      </label>
      <div className="flex gap-1.5 flex-wrap">
        {patterns.map((p) => (
          <button
            key={p.value}
            type="button"
            onClick={() => onPatternChange(p.value)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wider
              transition-all duration-300 border
              ${
                pattern === p.value
                  ? "border-blue-500/60 text-blue-300 shadow-lg shadow-blue-500/20"
                  : "border-white/10 text-gray-500 hover:border-white/20 hover:text-gray-300"
              }
            `}
            style={
              pattern === p.value
                ? { background: "rgba(59, 130, 246, 0.15)" }
                : { background: "rgba(255,255,255,0.03)" }
            }
          >
            {p.label}
          </button>
        ))}
      </div>
      {pattern && (
        <div className="animate-fade-in-up">
          <label className="block text-xs font-medium text-gray-400 mt-2 mb-1 uppercase tracking-wider">
            Repeat Until (optional)
          </label>
          <input
            type="date"
            className="input-field"
            value={endDate}
            onChange={(e) => onEndDateChange(e.target.value)}
          />
        </div>
      )}
    </div>
  );
}
