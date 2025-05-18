
import { cn } from "@/lib/utils";
import { AlertCircle } from "lucide-react";

interface KpiTilesProps {
  diseaseType: string;
  environmentalRisk: number;
  reportCount: number;
  outbreakRisk: number;
}

export function KpiTiles({
  diseaseType,
  environmentalRisk,
  reportCount,
  outbreakRisk,
}: KpiTilesProps) {
  const getRiskColor = (value: number) => {
    if (value <= 4) return "text-health-risk-low";
    if (value <= 8) return "text-health-risk-medium";
    return "text-health-risk-high";
  };

  const getOutbreakWarning = (risk: number) => {
    if (risk >= 8) {
      return (
        <div className="flex items-center gap-2 mt-2 text-health-risk-high">
          <AlertCircle size={16} />
          <span className="text-xs font-medium">High outbreak risk detected</span>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 animate-fade-in">
      <div className="health-card">
        <h3 className="text-sm font-semibold text-gray-500">Environmental Risk</h3>
        <div className="flex items-baseline mt-1">
          <span className={cn("text-2xl font-bold", getRiskColor(environmentalRisk))}>
            {environmentalRisk}
          </span>
          <span className="text-sm text-gray-500 ml-1">/10</span>
        </div>
      </div>

      <div className="health-card">
        <h3 className="text-sm font-semibold text-gray-500">Community Reports</h3>
        <div className="flex items-baseline mt-1">
          <span className="text-2xl font-bold text-health-blue">{reportCount}</span>
          <span className="text-sm text-gray-500 ml-1">Past 3 Weeks</span>
        </div>
      </div>

      <div className="health-card">
        <h3 className="text-sm font-semibold text-gray-500">Outbreak Risk Score</h3>
        <div className="flex items-baseline mt-1">
          <span className={cn("text-2xl font-bold", getRiskColor(outbreakRisk))}>
            {outbreakRisk}
          </span>
          <span className="text-sm text-gray-500 ml-1">/10</span>
        </div>
        {getOutbreakWarning(outbreakRisk)}
        <p className="text-xs text-gray-500 mt-1">
          Reflects likelihood based on environmental and community-reported data
        </p>
      </div>
    </div>
  );
}
