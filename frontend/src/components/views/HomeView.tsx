import React, { useState, useEffect } from 'react';
import { RefreshCw, Download, Volume2, Send } from 'lucide-react';
import { KPICard } from '../common/KPICard';
import { api } from '../../services/api';
import type { PlantaData, KPIsEjecutivos } from '../../types';

interface HomeViewProps {
  plantaData: PlantaData | null;
  onReload: () => void;
}

export const HomeView: React.FC<HomeViewProps> = ({ plantaData, onReload }) => {
  const [kpis, setKpis] = useState<KPIsEjecutivos | null>(null);
  const [loading, setLoading] = useState(false);
  const [range, setRange] = useState('30d');

  useEffect(() => {
    if (plantaData) {
      loadKPIs();
    }
  }, [plantaData, range]);

  const loadKPIs = async () => {
    try {
      setLoading(true);
      const data = await api.getExecutiveKPIs(range);
      setKpis(data);
    } catch (err) {
      console.error('Error loading KPIs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    try {
      const blob = await api.generatePDFReport(range);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Reporte_Ejecutivo_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Error generando PDF: ' + (err as any).message);
    }
  };

  const getStatusFromSystem = (estado: string): 'normal' | 'warning' | 'critical' => {
    if (estado === 'critico') return 'critical';
    if (estado === 'alerta') return 'warning';
    return 'normal';
  };

  if (!kpis || loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header con acciones */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Overview Ejecutivo</h2>
          <p className="text-gray-600 mt-1">Vista consolidada de performance</p>
        </div>
        <div className="flex gap-2">
          <select
            value={range}
            onChange={(e) => setRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="30d">Últimos 30 días</option>
            <option value="90d">Últimos 90 días</option>
            <option value="YTD">Año a la fecha</option>
            <option value="12m">Últimos 12 meses</option>
          </select>
          <button
            onClick={onReload}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Recargar
          </button>
          <button
            onClick={handleGeneratePDF}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            PDF
          </button>
        </div>
      </div>

      {/* KPIs Principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Energía Generada"
          value={`${(kpis.energia_real_kwh / 1000).toFixed(0)} MWh`}
          subtitle={`${kpis.desviacion_pct > 0 ? '+' : ''}${kpis.desviacion_pct.toFixed(1)}% vs esperado`}
          trend={kpis.desviacion_pct > 0 ? 'up' : kpis.desviacion_pct < 0 ? 'down' : 'stable'}
          status={kpis.desviacion_pct < -5 ? 'warning' : 'normal'}
        />
        
        <KPICard
          title="Performance Ratio (PR)"
          value={`${(kpis.pr_promedio * 100).toFixed(1)}%`}
          subtitle={`Objetivo: ${(plantaData!.planta.target_pr * 100).toFixed(1)}%`}
          status={
            kpis.pr_promedio < plantaData!.planta.target_pr * 0.9 ? 'critical' :
            kpis.pr_promedio < plantaData!.planta.target_pr * 0.95 ? 'warning' :
            'normal'
          }
        />
        
        <KPICard
          title="Disponibilidad"
          value={`${kpis.availability_promedio_pct.toFixed(1)}%`}
          subtitle={`Objetivo: ${plantaData!.planta.target_availability.toFixed(1)}%`}
          status={
            kpis.availability_promedio_pct < plantaData!.planta.target_availability - 5 ? 'critical' :
            kpis.availability_promedio_pct < plantaData!.planta.target_availability - 2 ? 'warning' :
            'normal'
          }
        />
        
        <KPICard
          title="Estado del Sistema"
          value={kpis.estado_sistema.toUpperCase()}
          subtitle={`Potencia actual: ${kpis.potencia_actual_kw.toFixed(0)} kW`}
          status={getStatusFromSystem(kpis.estado_sistema)}
        />
      </div>

      {/* KPIs Financieros */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KPICard
          title="Ingresos Estimados"
          value={`USD $${kpis.ingresos_estimados_usd.toLocaleString()}`}
          subtitle={`Margen bruto: ${kpis.margen_bruto_pct.toFixed(1)}%`}
        />
        
        <KPICard
          title="OPEX Estimado"
          value={`USD $${kpis.opex_estimado_usd.toLocaleString()}`}
          subtitle={`Costo/kWh: $${kpis.costo_por_kwh.toFixed(4)}`}
        />
        
        <KPICard
          title="CO₂ Evitado"
          value={`${(kpis.co2_evitado_kg / 1000).toFixed(1)} t`}
          subtitle="Toneladas de CO₂"
        />
      </div>

      {/* KPIs Operacionales */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <KPICard
          title="Backlog de Mantenimiento"
          value={`USD $${kpis.backlog_total_usd.toLocaleString()}`}
          subtitle={`${kpis.tickets_pendientes} tickets pendientes`}
          status={kpis.tickets_pendientes > 20 ? 'warning' : 'normal'}
        />
        
        <KPICard
          title="Tendencia Energética"
          value={kpis.tendencia === 'up' ? 'MEJORANDO' : kpis.tendencia === 'down' ? 'DECRECIENDO' : 'ESTABLE'}
          trend={kpis.tendencia}
        />
      </div>

      {/* Alertas */}
      {kpis.alertas_principales.length > 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg">
          <h3 className="font-bold text-yellow-900 mb-2">⚠️ Alertas Principales</h3>
          <ul className="list-disc list-inside space-y-1">
            {kpis.alertas_principales.map((alerta, idx) => (
              <li key={idx} className="text-yellow-800 text-sm">{alerta}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
