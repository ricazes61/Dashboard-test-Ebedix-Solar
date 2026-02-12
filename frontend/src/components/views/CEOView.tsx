import React, { useState, useEffect } from 'react';
import { TrendingUp, Leaf } from 'lucide-react';
import { KPICard } from '../common/KPICard';
import { api } from '../../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { PlantaData, KPIsEjecutivos, RealtimeDataPoint } from '../../types';

interface CEOViewProps {
  plantaData: PlantaData | null;
}

export const CEOView: React.FC<CEOViewProps> = ({ plantaData }) => {
  const [kpis, setKpis] = useState<KPIsEjecutivos | null>(null);
  const [series, setSeries] = useState<RealtimeDataPoint[]>([]);
  const [range, setRange] = useState('30d');

  useEffect(() => {
    if (plantaData) {
      loadData();
    }
  }, [plantaData, range]);

  const loadData = async () => {
    try {
      const [kpisData, seriesData] = await Promise.all([
        api.getExecutiveKPIs(range),
        api.getRealtimeSeries(24)
      ]);
      setKpis(kpisData);
      setSeries(seriesData);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (!kpis) return <div>Cargando...</div>;

  const chartData = series.slice(-48).map(point => ({
    time: new Date(point.timestamp).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' }),
    potencia: (point.potencia_kw / 1000).toFixed(2),
  }));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Vista CEO</h2>
          <p className="text-gray-600">Indicadores estratégicos y sostenibilidad</p>
        </div>
        <select
          value={range}
          onChange={(e) => setRange(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value="30d">30 días</option>
          <option value="90d">90 días</option>
          <option value="YTD">YTD</option>
          <option value="12m">12 meses</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KPICard
          title="Energía Real vs Esperada"
          value={`${kpis.desviacion_pct > 0 ? '+' : ''}${kpis.desviacion_pct.toFixed(1)}%`}
          subtitle={`${(kpis.energia_real_kwh / 1000).toFixed(0)} MWh generados`}
          trend={kpis.tendencia}
          icon={<TrendingUp />}
        />
        
        <KPICard
          title="CO₂ Evitado"
          value={`${(kpis.co2_evitado_kg / 1000).toFixed(1)} t`}
          subtitle="Impacto ambiental positivo"
          icon={<Leaf className="w-5 h-5 text-green-600" />}
          status="normal"
        />
        
        <KPICard
          title="Performance General"
          value={`${(kpis.pr_promedio * 100).toFixed(1)}%`}
          subtitle="Performance Ratio"
          status={kpis.pr_promedio < 0.75 ? 'critical' : kpis.pr_promedio < 0.80 ? 'warning' : 'normal'}
        />
      </div>

      {kpis.alertas_principales.length > 0 && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg">
          <h3 className="font-bold text-red-900 mb-2">🚨 Alertas Críticas para Atención</h3>
          <ul className="list-disc list-inside space-y-1">
            {kpis.alertas_principales.map((alerta, idx) => (
              <li key={idx} className="text-red-800">{alerta}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-bold mb-4">Potencia en Tiempo Real (últimas 4 horas)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis label={{ value: 'MW', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="potencia" stroke="#3b82f6" name="Potencia (MW)" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
