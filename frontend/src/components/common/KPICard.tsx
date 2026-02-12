import React from 'react';
import { TrendingUp, TrendingDown, Minus, AlertCircle } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'stable';
  status?: 'normal' | 'warning' | 'critical';
  icon?: React.ReactNode;
  formatValue?: (val: string | number) => string;
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  subtitle,
  trend,
  status = 'normal',
  icon,
  formatValue
}) => {
  const displayValue = formatValue ? formatValue(value) : value;

  const statusColors = {
    normal: 'border-green-500 bg-green-50',
    warning: 'border-yellow-500 bg-yellow-50',
    critical: 'border-red-500 bg-red-50'
  };

  const trendIcons = {
    up: <TrendingUp className="w-5 h-5 text-green-600" />,
    down: <TrendingDown className="w-5 h-5 text-red-600" />,
    stable: <Minus className="w-5 h-5 text-gray-600" />
  };

  return (
    <div className={`border-l-4 rounded-lg p-4 shadow-sm bg-white ${statusColors[status]}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{displayValue}</p>
          {subtitle && (
            <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
        <div className="flex flex-col items-end gap-2">
          {icon && <div className="text-gray-600">{icon}</div>}
          {trend && <div>{trendIcons[trend]}</div>}
          {status === 'critical' && <AlertCircle className="w-5 h-5 text-red-600" />}
          {status === 'warning' && <AlertCircle className="w-5 h-5 text-yellow-600" />}
        </div>
      </div>
    </div>
  );
};
