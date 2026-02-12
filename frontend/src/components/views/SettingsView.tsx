import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, RefreshCw, FolderOpen, CheckCircle, XCircle, Download, Volume2, Send } from 'lucide-react';
import { api } from '../../services/api';
import type { Settings, ReloadResponse, TTSResponse, WhatsAppResponse } from '../../types';

interface SettingsViewProps {
  onDataReloaded: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({ onDataReloaded }) => {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [dataFolder, setDataFolder] = useState('');
  const [reloadResult, setReloadResult] = useState<ReloadResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [audioPath, setAudioPath] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('+549');
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await api.getSettings();
      setSettings(data);
      setDataFolder(data.data_folder);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  const handleUpdateFolder = async () => {
    try {
      setLoading(true);
      const data = await api.updateSettings(dataFolder);
      setSettings(data);
      setMessage('✅ Folder configurado correctamente');
    } catch (err: any) {
      setMessage('❌ Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleReloadData = async () => {
    try {
      setLoading(true);
      setMessage('');
      const result = await api.reloadData();
      setReloadResult(result);
      if (result.success) {
        setMessage('✅ Datos recargados exitosamente');
        onDataReloaded();
      } else {
        setMessage('⚠️ Algunos archivos no se pudieron cargar');
      }
    } catch (err: any) {
      setMessage('❌ Error recargando datos: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    try {
      setLoading(true);
      const blob = await api.generatePDFReport('30d');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Reporte_Ejecutivo_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      setMessage('✅ PDF generado y descargado');
    } catch (err: any) {
      setMessage('❌ Error generando PDF: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateTTS = async () => {
    try {
      setLoading(true);
      const result: TTSResponse = await api.generateTTSAudio();
      setAudioPath(result.audio_path);
      setMessage(`✅ Audio generado: ${result.filename}`);
    } catch (err: any) {
      setMessage('❌ Error generando audio: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSendWhatsApp = async () => {
    if (!audioPath) {
      setMessage('⚠️ Primero genera el audio TTS');
      return;
    }
    if (!phoneNumber.startsWith('+')) {
      setMessage('⚠️ El número debe comenzar con + (formato E.164)');
      return;
    }

    try {
      setLoading(true);
      const result: WhatsAppResponse = await api.sendWhatsAppAudio(phoneNumber, audioPath);
      if (result.mode === 'simulation') {
        setMessage(`🚧 SIMULACIÓN: ${result.message}`);
      } else {
        setMessage(`✅ WhatsApp enviado - SID: ${result.sid}`);
      }
    } catch (err: any) {
      setMessage('❌ Error enviando WhatsApp: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
          <SettingsIcon className="w-8 h-8" />
          Configuración
        </h2>
        <p className="text-gray-600 mt-1">Administrar datos y opciones del sistema</p>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${
          message.includes('✅') ? 'bg-green-50 text-green-800' :
          message.includes('❌') ? 'bg-red-50 text-red-800' :
          'bg-yellow-50 text-yellow-800'
        }`}>
          {message}
        </div>
      )}

      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 className="text-xl font-bold flex items-center gap-2">
          <FolderOpen className="w-5 h-5" />
          Folder de Datos
        </h3>
        <p className="text-sm text-gray-600">
          Ruta local donde se encuentran los archivos CSV/Excel de entrada
        </p>
        <div className="flex gap-2">
          <input
            type="text"
            value={dataFolder}
            onChange={(e) => setDataFolder(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="./data/input"
          />
          <button
            onClick={handleUpdateFolder}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Guardar
          </button>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 className="text-xl font-bold flex items-center gap-2">
          <RefreshCw className="w-5 h-5" />
          Recarga de Datos
        </h3>
        <button
          onClick={handleReloadData}
          disabled={loading}
          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          {loading ? 'Recargando...' : 'Recargar Datos Ahora'}
        </button>

        {reloadResult && (
          <div className="mt-4 space-y-2">
            <p className="font-medium">Última recarga: {new Date(reloadResult.last_reload).toLocaleString('es-AR')}</p>
            <div className="space-y-1">
              {Object.entries(reloadResult.files_loaded).map(([file, count]) => (
                <div key={file} className="flex items-center gap-2 text-sm">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>{file}: {count} registros</span>
                </div>
              ))}
            </div>
            {reloadResult.errors.length > 0 && (
              <div className="mt-2">
                {reloadResult.errors.map((error, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm text-red-600">
                    <XCircle className="w-4 h-4" />
                    <span>{error}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 className="text-xl font-bold flex items-center gap-2">
          <Download className="w-5 h-5" />
          Reportes y Notificaciones
        </h3>
        
        <div className="space-y-3">
          <button
            onClick={handleGeneratePDF}
            disabled={loading}
            className="w-full px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <Download className="w-5 h-5" />
            Generar Reporte PDF Ejecutivo
          </button>

          <button
            onClick={handleGenerateTTS}
            disabled={loading}
            className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <Volume2 className="w-5 h-5" />
            Generar Audio TTS (Resumen Ejecutivo)
          </button>

          {audioPath && (
            <div className="p-4 bg-purple-50 rounded-lg">
              <p className="text-sm font-medium text-purple-900 mb-2">♫ Audio generado: {audioPath}</p>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="+5491112345678"
                  className="flex-1 px-3 py-2 border rounded-lg text-sm"
                />
                <button
                  onClick={handleSendWhatsApp}
                  disabled={loading}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  Enviar por WhatsApp
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-lg">
        <h4 className="font-bold text-blue-900 mb-2">📌 Archivos Requeridos</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• <code>Parametros_Planta.xlsx</code> (hojas: Planta, Equipos, Umbrales)</li>
          <li>• <code>Historico_Performance.csv</code></li>
          <li>• <code>Tickets_Mantenimiento.csv</code></li>
        </ul>
      </div>
    </div>
  );
};