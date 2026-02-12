import axios, { AxiosInstance } from 'axios';
import type {
  PlantaData,
  KPIsEjecutivos,
  RealtimeDataPoint,
  Ticket,
  Settings,
  ReloadResponse,
  TTSResponse,
  WhatsAppResponse
} from '../types';

class API {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  // Health
  async healthCheck(): Promise<{ status: string }> {
    const { data } = await this.client.get('/health');
    return data;
  }

  // Settings
  async getSettings(): Promise<Settings> {
    const { data } = await this.client.get('/settings');
    return data;
  }

  async updateSettings(data_folder: string): Promise<Settings> {
    const { data } = await this.client.post('/settings', { data_folder });
    return data;
  }

  // Data
  async reloadData(): Promise<ReloadResponse> {
    const { data } = await this.client.post('/data/reload');
    return data;
  }

  async getPlantData(): Promise<PlantaData> {
    const { data } = await this.client.get('/plant');
    return data;
  }

  async getExecutiveKPIs(range: string = '30d'): Promise<KPIsEjecutivos> {
    const { data } = await this.client.get('/kpis/exec', { params: { range } });
    return data;
  }

  async getRealtimeSeries(hours: number = 24): Promise<RealtimeDataPoint[]> {
    const { data } = await this.client.get('/series/realtime', { params: { hours } });
    return data;
  }

  async getTickets(
    status?: string,
    sort: string = 'costo_desc',
    limit?: number
  ): Promise<Ticket[]> {
    const { data } = await this.client.get('/tickets', {
      params: { status, sort, limit }
    });
    return data;
  }

  // Reports
  async generatePDFReport(range: string = '30d'): Promise<Blob> {
    const { data } = await this.client.post(
      '/report/pdf',
      {},
      {
        params: { range },
        responseType: 'blob'
      }
    );
    return data;
  }

  async generateTTSAudio(text?: string): Promise<TTSResponse> {
    const { data } = await this.client.post('/report/tts', { text });
    return data;
  }

  async sendWhatsAppAudio(
    to_phone: string,
    audio_path: string
  ): Promise<WhatsAppResponse> {
    const { data } = await this.client.post('/whatsapp/send-audio', {
      to_phone,
      audio_path
    });
    return data;
  }

  async sendWhatsAppText(to_phone: string, message: string): Promise<WhatsAppResponse> {
    const { data } = await this.client.post('/whatsapp/send-text', null, {
      params: { to_phone, message }
    });
    return data;
  }
}

export const api = new API();
