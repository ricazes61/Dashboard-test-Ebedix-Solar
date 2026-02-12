import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp } from 'lucide-react';
import { KPICard } from '../common/KPICard';
import { api } from '../../services/api';
import type { PlantaData, KPIsEjecutivos } from '../../types';

interface CFOViewProps {
  plantaData: PlantaData | null;
}

export const CFOView: React.FC<CFOViewProps> = ({ plantaData }) => {
  const [kpis, setKpis] = useState<KPIsEjecutivos | null>(null);
  const [range, setRange] = useState('30d');

  useEffect(() => {
    if (plantaData) {
      api.getExecutiveKPIs(range).then(setKpis);
    }
  }, [plantaData, range]);

  if (!kpis) return <div>Cargando...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Vista CFO</h2>
          <p className="text-gray-600">Indicadores financieros y rentabilidad</p>
        </div>
        <select value={range} onChange={(e) => setRange(e.target.value)} className="px-4 py-2 border rounded-lg">
          <option value="30d">30 días</option>
          <option value="90d">90 días</option>
          <option value="YTD">YTD</option>
          <option value="12m">12 meses</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Ingresos Estimados"
          value={`$${kpis.ingresos_estimados_usd.toLocaleString()}`}
          icon={<DollarSign className="w-5 h-5 text-green-600" />}
        />
        <KPICard
          title="OPEX"
          value={`$${kpis.opex_estimado_usd.toLocaleString()}`}
        />
        <KPICard
          title="Margen Bruto"
          value={`${kpis.margen_bruto_pct.toFixed(1)}%`}
          subtitle={`$${kpis.margen_bruto_usd.toLocaleString()}`}
          status={kpis.margen_bruto_pct < 50 ? 'warning' : 'normal'}
        />
        <KPICard
          title="Costo por kWh"
          value={`$${kpis.costo_por_kwh.toFixed(4)}`}
        />
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-bold mb-4">Resumen Financiero</h3>
        <div className="space-y-2">
          <div className="flex justify-between py-2 border-b">
            <span className="font-medium">Ingresos totales:</span>
            <span className="text-green-600 font-bold">${kpis.ingresos_estimados_usd.toLocaleString()}</span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span className="font-medium">OPEX:</span>
            <span className="text-red-600">-${kpis.opex_estimado_usd.toLocaleString()}</span>
          </div>
          <div className="flex justify-between py-2 border-b font-bold text-lg">
            <span>Margen bruto:</span>
            <span className="text-blue-600">${kpis.margen_bruto_usd.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};