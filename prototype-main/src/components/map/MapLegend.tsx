
import { cn } from "@/lib/utils";

interface MapLegendProps {
  diseaseType: string;
}

export function MapLegend({ diseaseType }: MapLegendProps) {
  // Get the environmental factor based on disease type
  const getEnvironmentalFactor = (disease: string) => {
    switch (disease) {
      case "Influenza":
        return "Air Pollution & Temperature";
      case "Norovirus":
        return "Soil Moisture";
      case "COVID-19":
        return "Air Pollution & Population Density";
      case "Heatstroke":
        return "Land Surface Temperature";
      default:
        return "Environmental Risk";
    }
  };

  return (
    <div className="absolute bottom-4 right-4 bg-white bg-opacity-90 p-3 rounded-lg shadow-md z-10 text-sm animate-fade-in">
      <h4 className="font-bold mb-2">{getEnvironmentalFactor(diseaseType)} Risk</h4>
      <div className="flex items-center gap-2 mb-1">
        <div className="w-4 h-4 rounded-full bg-health-risk-low"></div>
        <span>Low Risk (0-4)</span>
      </div>
      <div className="flex items-center gap-2 mb-1">
        <div className="w-4 h-4 rounded-full bg-health-risk-medium"></div>
        <span>Moderate Risk (5-8)</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-health-risk-high"></div>
        <span>High Risk (9-10)</span>
      </div>
    </div>
  );
}
