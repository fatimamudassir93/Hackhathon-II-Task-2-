"use client";

const offsets = [
  { value: 15, label: "15 min before" },
  { value: 30, label: "30 min before" },
  { value: 60, label: "1 hour before" },
  { value: 180, label: "3 hours before" },
  { value: 1440, label: "1 day before" },
] as const;

interface ReminderToggleProps {
  enabled: boolean;
  offsetMinutes: number;
  onEnabledChange: (enabled: boolean) => void;
  onOffsetChange: (minutes: number) => void;
}

export default function ReminderToggle({
  enabled,
  offsetMinutes,
  onEnabledChange,
  onOffsetChange,
}: ReminderToggleProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-3">
        <button
          type="button"
          role="switch"
          aria-checked={enabled}
          onClick={() => onEnabledChange(!enabled)}
          className={`toggle-switch ${enabled ? "active" : ""}`}
        >
          <span className="toggle-knob" />
        </button>
        <label className="text-xs font-medium text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          Remind Me
        </label>
      </div>
      {enabled && (
        <div className="animate-fade-in-up">
          <select
            className="input-field text-sm"
            value={offsetMinutes}
            onChange={(e) => onOffsetChange(Number(e.target.value))}
          >
            {offsets.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}
