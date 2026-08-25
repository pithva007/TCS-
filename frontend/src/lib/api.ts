export interface Source {
  file: string;
  section: string;
  excerpt: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  tier_used: string;
  confidence: number;
}

export interface HealthResponse {
  status: string;
  data_files: number;
  vectors_count: number;
  last_ingestion: string;
}

export interface AnalyticsSummary {
  total_queries: number;
  popular_topics: { topic: string; count: number }[];
  avg_response_time_ms: number;
}

export interface Building {
  id: string;
  name: string;
  category: "academic" | "facility" | "amenity" | string;
  description: string;
  facilities: string[];
  location: { lat: number; lng: number };
}

export interface CampusResponse {
  buildings: Building[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = {
  chat: async (message: string, sessionId: string): Promise<ChatResponse> => {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    if (!res.ok) {
      throw new Error(`Chat API error: ${res.statusText}`);
    }
    return res.json();
  },

  health: async (): Promise<HealthResponse> => {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    if (!res.ok) throw new Error("Health check failed");
    return res.json();
  },

  analyticsSummary: async (): Promise<AnalyticsSummary> => {
    const res = await fetch(`${API_BASE_URL}/api/analytics/summary`);
    if (!res.ok) throw new Error("Analytics fetch failed");
    return res.json();
  },

  campusBuildings: async (): Promise<CampusResponse> => {
    const res = await fetch(`${API_BASE_URL}/api/campus/buildings`);
    if (!res.ok) throw new Error("Campus buildings fetch failed");
    return res.json();
  },
};
