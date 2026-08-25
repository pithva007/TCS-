"use client";

import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { api, Building } from "@/lib/api";
import { MapPin, Navigation, Info, Layers } from "lucide-react";

export default function CampusMapPage() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState<string>("all");

  const NIRMA_COORDS: [number, number] = [72.5413, 23.1332]; // [lng, lat]

  useEffect(() => {
    async function loadBuildings() {
      try {
        const res = await api.campusBuildings();
        setBuildings(res.buildings);
      } catch (e) {
        console.error("Failed to fetch buildings", e);
      } finally {
        setLoading(false);
      }
    }
    loadBuildings();
  }, []);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }
        },
        layers: [
          {
            id: "osm-layer",
            type: "raster",
            source: "osm",
            minzoom: 0,
            maxzoom: 19
          }
        ]
      },
      center: NIRMA_COORDS,
      zoom: 16.5,
      pitch: 45,
      bearing: -17.6,
      antialias: true
    });

    map.current.addControl(new maplibregl.NavigationControl(), "top-right");

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    if (!map.current || buildings.length === 0) return;

    // Wait for map to load before adding markers if it just initialized
    const addMarkers = () => {
      const markerElements = document.querySelectorAll(".custom-marker");
      markerElements.forEach(el => el.remove());

      buildings.forEach((building) => {
        if (activeCategory !== "all" && building.category !== activeCategory) return;

        const el = document.createElement("div");
        el.className = "custom-marker";
        
        let color = "#10b981"; // emerald default
        if (building.category === "facility") color = "#3b82f6"; // blue
        if (building.category === "amenity") color = "#f59e0b"; // amber

        el.innerHTML = `
          <div style="
            width: 24px; 
            height: 24px; 
            background-color: ${color}; 
            border: 2px solid white; 
            border-radius: 50%;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-center;
            transition: transform 0.2s;
          "></div>
        `;

        el.addEventListener("mouseenter", () => {
          el.style.transform = "scale(1.2)";
        });
        el.addEventListener("mouseleave", () => {
          el.style.transform = "scale(1)";
        });

        const popup = new maplibregl.Popup({ offset: 25, closeButton: false, className: "custom-popup" })
          .setHTML(`
            <div class="p-3 max-w-[250px]">
              <h3 class="font-bold text-gray-900 text-lg mb-1">${building.name}</h3>
              <span class="inline-block px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full uppercase tracking-wider mb-2 font-medium">
                ${building.category}
              </span>
              <p class="text-sm text-gray-600 mb-2">${building.description}</p>
              ${building.facilities.length > 0 ? `
                <div class="text-xs text-gray-500">
                  <strong>Facilities:</strong> ${building.facilities.join(", ")}
                </div>
              ` : ''}
            </div>
          `);

        new maplibregl.Marker(el)
          .setLngLat([building.location.lng, building.location.lat])
          .setPopup(popup)
          .addTo(map.current!);
      });
    };

    if (map.current.loaded()) {
      addMarkers();
    } else {
      map.current.on("load", addMarkers);
    }
  }, [buildings, activeCategory]);

  const flyTo = (lng: number, lat: number) => {
    map.current?.flyTo({
      center: [lng, lat],
      zoom: 18,
      essential: true,
      pitch: 60
    });
  };

  const categories = ["all", ...Array.from(new Set(buildings.map(b => b.category)))];

  return (
    <div className="flex flex-1 h-[calc(100vh-64px)] overflow-hidden relative bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 flex-shrink-0 bg-white border-r border-card-border flex flex-col z-10 shadow-lg">
        <div className="p-5 border-b border-card-border bg-gradient-to-br from-surface-soft to-white">
          <h2 className="font-playfair text-xl font-bold text-text-primary flex items-center gap-2">
            <Navigation className="w-5 h-5 text-primary" />
            Campus Navigator
          </h2>
          <p className="text-sm text-text-secondary mt-1">
            Explore Nirma University 3D campus
          </p>
        </div>
        
        <div className="p-4 border-b border-card-border">
          <div className="flex items-center gap-2 mb-3">
            <Layers className="w-4 h-4 text-text-secondary" />
            <span className="text-xs font-semibold uppercase text-text-secondary">Filter by</span>
          </div>
          <select 
            value={activeCategory}
            onChange={(e) => setActiveCategory(e.target.value)}
            className="w-full p-2 bg-surface-soft border border-card-border rounded-lg text-sm text-text-primary focus:outline-none focus:ring-2 focus:ring-primary"
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {loading ? (
            <div className="animate-pulse space-y-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-20 bg-gray-100 rounded-lg"></div>
              ))}
            </div>
          ) : (
            buildings
              .filter(b => activeCategory === "all" || b.category === activeCategory)
              .map((b) => (
                <button
                  key={b.id}
                  onClick={() => flyTo(b.location.lng, b.location.lat)}
                  className="w-full text-left p-3 rounded-xl border border-transparent hover:border-primary/20 hover:bg-surface-soft transition-all group shadow-sm bg-white ring-1 ring-black/5"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-1">
                      <MapPin className="w-5 h-5 text-primary group-hover:scale-110 transition-transform" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-text-primary text-sm group-hover:text-primary transition-colors">
                        {b.name}
                      </h4>
                      <p className="text-xs text-text-secondary mt-1 line-clamp-2">
                        {b.description}
                      </p>
                    </div>
                  </div>
                </button>
            ))
          )}
        </div>
      </div>

      {/* Map Container */}
      <div className="flex-1 relative">
        <div ref={mapContainer} className="absolute inset-0" />
        
        {/* Map UI Overlay */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur px-4 py-2 rounded-full shadow-lg border border-card-border text-xs font-medium flex items-center gap-2 pointer-events-none text-text-secondary">
          <Info className="w-4 h-4 text-primary" />
          Hold Right-Click to Rotate & Pitch
        </div>
      </div>
    </div>
  );
}
