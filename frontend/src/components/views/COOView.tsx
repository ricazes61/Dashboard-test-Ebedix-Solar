import React, { useState, useEffect } from 'react';
import { Wrench, AlertTriangle } from 'lucide-react';
import { KPICard } from '../common/KPICard';
import { api } from '../../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { PlantaData, KPIsEjecutivos, Ticket, RealtimeDataPoint } from '../../types';

interface COOViewProps {
  plantaData: PlantaData | null;
}

export const COOView: React.FC<COOViewProps> = ({ plantaData }) => {
  const [kpis, setKpis] = useState<KPIsEjecutivos | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [series, setSeries] = useState<RealtimeDataPoint[]>([]);

  useEffect(() => {
    if (plantaData) {
      loadData();
      const interval = setInterval(loadRealtime, 15000);
      return () => clearInterval(interval);
    }
  }, [plantaData]);

  const loadData = async () => {
    try {
      const [kpisData, ticketsData, seriesData] = await Promise.all([
        api.getExecutiveKPIs('30d'),
        api.getTickets('pendiente', 'costo_desc', 10),
        api.getRealtimeSeries(1)
      ]);
      setKpis(kpisData);
      setTickets(ticketsData);
      setSeries(seriesData);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  const loadRealtime = async () => {
    try {
      const data = await api.getRealtimeSeries(1);
      setSeries(data);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (!kpis) return <div>Cargando...</div>;

  const currentPower = series.length > 0 ? series[series.length - 1] : null;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Vista COO</h2>
        <p className="text-gray-600">Operaciones y mantenimiento</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard
          title="PR Promedio"
          value={`${(kpis.pr_promedio * 100).toFixed(1)}%`}
          subtitle={`Objetivo: ${(plantaData!.planta.target_pr * 100).toFixed(1)}%`}
          status={kpis.pr_promedio < plantaData!.planta.target_pr * 0.9 ? 'critical' : 'normal'}
        />
        <KPICard
          title="Disponibilidad"
          value={`${kpis.availability_promedio_pct.toFixed(1)}%`}
          status={kpis.availability_promedio_pct < 95 ? 'warning' : 'normal'}
        />
        <KPICard
          title="Potencia Actual"
          value={currentPower ? `${(currentPower.potencia_kw / 1000).toFixed(1)} MW` : 'N/A'}
          subtitle="Tiempo real"
        />
        <KPICard
          title="Backlog Mantenimiento"
          value={`$${kpis.backlog_total_usd.toLocaleString()}`}
          subtitle={`${kpis.tickets_pendientes} tickets`}
          status={kpis.tickets_pendientes > 20 ? 'warning' : 'normal'}
        />
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Wrench className="w-5 h-5" />
          Top 10 Tickets por Costo (Pendientes)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">ID</th>
                <th className="px-4 py-2 text-left">Descripción</th>
                <th className="px-4 py-2 text-left">Estado</th>
                <th className="px-4 py-2 text-left">Criticidad</th>
                <th className="px-4 py-2 text-right">Costo (USD)</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((ticket) => (
                <tr key={ticket.ticket_id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2 font-mono text-xs">{ticket.ticket_id}</td>
                  <td className="px-4 py-2">{ticket.descripcion.substring(0, 50)}{ticket.descripcion.length > 50 ? '...' : ''}</td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded text-xs ${
                      ticket.estado === 'Bloqueado' ? 'bg-red-100 text-red-800' :
                      ticket.estado === 'En Progreso' ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {ticket.estado}
                    </span>
                  </td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded text-xs ${
                      ticket.criticidad === 'Crítica' || ticket.criticidad === 'Alta' ? 'bg-red-100 text-red-800' :
                      ticket.criticidad === 'Media' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {ticket.criticidad}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-right font-bold">${ticket.costo_estimado_usd.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};