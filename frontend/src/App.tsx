import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { Home, Briefcase, DollarSign, Settings as SettingsIcon, Sun } from 'lucide-react';
import { CEOView } from './components/views/CEOView';
import { CFOView } from './components/views/CFOView';
import { COOView } from './components/views/COOView';
import { SettingsView } from './components/views/SettingsView';
import { HomeView } from './components/views/HomeView';
import { api } from './services/api';
import type { PlantaData } from './types';

function App() {
  const [plantaData, setPlantaData] = useState<PlantaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await api.getPlantData();
      setPlantaData(data);
      setError(null);
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError(err.response?.data?.detail || 'Error cargando datos. Configurar en Settings.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-gradient-to-r from-blue-900 to-blue-700 text-white shadow-lg">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Sun className="w-10 h-10 text-yellow-400" />
                <div>
                  <h1 className="text-2xl font-bold">
                    {plantaData?.planta.nombre_planta || 'Solar PV Analytics'}
                  </h1>
                  <p className="text-sm text-blue-200">
                    {plantaData && `${plantaData.planta.ciudad}, ${plantaData.planta.provincia_estado}`}
                  </p>
                </div>
              </div>
              {plantaData && (
                <div className="text-right text-sm">
                  <p className="font-semibold">{plantaData.planta.potencia_dc_mwp} MWp DC</p>
                  <p className="text-blue-200">{plantaData.planta.potencia_ac_mw} MW AC</p>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Navigation */}
        <nav className="bg-white border-b border-gray-200 shadow-sm">
          <div className="container mx-auto px-4">
            <div className="flex gap-6">
              <NavLink to="/" icon={<Home className="w-4 h-4" />} label="Overview" />
              <NavLink to="/ceo" icon={<Briefcase className="w-4 h-4" />} label="CEO" />
              <NavLink to="/cfo" icon={<DollarSign className="w-4 h-4" />} label="CFO" />
              <NavLink to="/coo" icon={<SettingsIcon className="w-4 h-4" />} label="COO" />
              <NavLink to="/settings" icon={<SettingsIcon className="w-4 h-4" />} label="Configuración" />
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="container mx-auto px-4 py-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Cargando...</p>
              </div>
            </div>
          ) : error ? (
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
              <p className="text-yellow-800 font-medium">⚠️ {error}</p>
              <p className="text-yellow-700 text-sm mt-2">
                Por favor, configure el folder de datos en la sección de Configuración.
              </p>
              <Link to="/settings" className="text-blue-600 hover:underline text-sm mt-2 inline-block">
                Ir a Configuración →
              </Link>
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<HomeView plantaData={plantaData} onReload={loadData} />} />
              <Route path="/ceo" element={<CEOView plantaData={plantaData} />} />
              <Route path="/cfo" element={<CFOView plantaData={plantaData} />} />
              <Route path="/coo" element={<COOView plantaData={plantaData} />} />
              <Route path="/settings" element={<SettingsView onDataReloaded={loadData} />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          )}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="container mx-auto px-4 py-6">
            <div className="text-center text-sm text-gray-600">
              <p>Solar PV Analytics © 2024 - Vreadynow Digital Twin Platform</p>
              <p className="text-xs text-gray-500 mt-1">
                Demo ejecutable localmente para análisis de plantas solares fotovoltaicas
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

interface NavLinkProps {
  to: string;
  icon: React.ReactNode;
  label: string;
}

const NavLink: React.FC<NavLinkProps> = ({ to, icon, label }) => {
  return (
    <Link to={to} className="flex items-center gap-2 py-3 px-2 border-b-2 border-transparent hover:border-blue-600 hover:text-blue-600 transition-colors text-gray-700 font-medium">
      {icon}
      <span>{label}</span>
    </Link>
  );
};

export default App;
