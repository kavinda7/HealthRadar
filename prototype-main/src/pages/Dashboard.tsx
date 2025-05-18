
import { useState, useEffect } from "react";
import { Select } from "@/components/ui/select";
import { HealthMap } from "@/components/map/HealthMap";
import { KpiTiles } from "@/components/map/KpiTiles";
import { NewsWidget } from "@/components/news/NewsWidget";
import { Thermometer, Bug, Droplet, Sun } from "lucide-react";

interface DiseaseOption {
  value: string;
  label: string;
  icon: React.ReactNode;
}

interface LocationOption {
  value: string;
  label: string;
}

export default function Dashboard() {
  const [diseaseType, setDiseaseType] = useState<string>("Influenza");
  const [location, setLocation] = useState<string>("Oulu");
  const [environmentalRisk, setEnvironmentalRisk] = useState<number>(5);
  const [reportCount, setReportCount] = useState<number>(12);
  const [outbreakRisk, setOutbreakRisk] = useState<number>(6);

  const diseaseOptions: DiseaseOption[] = [
    { value: "Influenza", label: "Influenza", icon: <Thermometer className="h-4 w-4 mr-2" /> },
    { value: "Norovirus", label: "Norovirus", icon: <Bug className="h-4 w-4 mr-2" /> },
    { value: "COVID-19", label: "COVID-19", icon: <Bug className="h-4 w-4 mr-2" /> },
    { value: "Heatstroke", label: "Heatstroke", icon: <Sun className="h-4 w-4 mr-2" /> },
  ];

  const locationOptions: LocationOption[] = [
    { value: "Oulu", label: "Oulu" },
    { value: "Helsinki", label: "Helsinki" },
    { value: "Tampere", label: "Tampere" },
    { value: "Turku", label: "Turku" },
    { value: "Jyväskylä", label: "Jyväskylä" },
  ];

  // Update KPIs when disease or location changes
  useEffect(() => {
    // Simulate data calculation based on selected parameters
    const calculateRisks = () => {
      let envRisk, reports, outRisk;
      
      switch (diseaseType) {
        case "Influenza":
          envRisk = Math.floor(Math.random() * 4) + 4;  // 4-7
          reports = Math.floor(Math.random() * 15) + 8;  // 8-22
          outRisk = Math.min(10, Math.floor(envRisk * 0.7 + reports * 0.3));
          break;
        case "Norovirus":
          envRisk = Math.floor(Math.random() * 3) + 6;  // 6-8
          reports = Math.floor(Math.random() * 10) + 2;  // 2-11
          outRisk = Math.min(10, Math.floor(envRisk * 0.6 + reports * 0.4));
          break;
        case "COVID-19":
          envRisk = Math.floor(Math.random() * 4) + 5;  // 5-8
          reports = Math.floor(Math.random() * 20) + 5;  // 5-24
          outRisk = Math.min(10, Math.floor(envRisk * 0.5 + reports * 0.5));
          break;
        case "Heatstroke":
          envRisk = Math.floor(Math.random() * 5) + 5;  // 5-9
          reports = Math.floor(Math.random() * 6) + 1;  // 1-6
          outRisk = Math.min(10, Math.floor(envRisk * 0.8 + reports * 0.2));
          break;
        default:
          envRisk = 5;
          reports = 10;
          outRisk = 5;
      }
      
      // Inject some location-based variation
      if (location === "Helsinki") {
        reports = Math.min(30, reports + 5);  // More reports in capital
        outRisk = Math.min(10, outRisk + 1);  // Higher risk due to population
      }
      
      setEnvironmentalRisk(envRisk);
      setReportCount(reports);
      setOutbreakRisk(outRisk);
    };
    
    calculateRisks();
  }, [diseaseType, location]);

  return (
    <div className="container max-w-4xl mx-auto pt-4 pb-20 md:pt-20 md:pb-4 px-4">
      <div className="flex flex-col md:flex-row gap-4 mb-4">
        <div className="w-full md:w-1/2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Disease Type</label>
          <select
            value={diseaseType}
            onChange={(e) => setDiseaseType(e.target.value)}
            className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-health-blue"
          >
            {diseaseOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="w-full md:w-1/2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
          <select
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-health-blue"
          >
            {locationOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <KpiTiles 
        diseaseType={diseaseType}
        environmentalRisk={environmentalRisk}
        reportCount={reportCount}
        outbreakRisk={outbreakRisk}
      />

      <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
        <HealthMap diseaseType={diseaseType} location={location} />
      </div>
      
      {/* Add the NewsWidget component */}
      <NewsWidget diseaseType={diseaseType} location={location} />
      
      <div className="mt-4 text-sm text-gray-500">
        <h3 className="font-medium text-gray-700 mb-1">About {diseaseType}</h3>
        {diseaseType === "Influenza" && (
          <p>Key symptoms include fever, cough, sore throat, and nasal congestion. The map shows air pollution and temperature data that may affect spread.</p>
        )}
        {diseaseType === "Norovirus" && (
          <p>Key symptoms include nausea, vomiting, diarrhea, and headache. The map shows soil moisture data that may affect norovirus persistence.</p>
        )}
        {diseaseType === "COVID-19" && (
          <p>Key symptoms include fever, cough, nasal congestion, and fatigue. The map shows air pollution and population density data that may affect spread.</p>
        )}
        {diseaseType === "Heatstroke" && (
          <p>Key symptoms include headache, nausea, dizziness, and confusion. The map shows land surface temperature data with urban heat island effects.</p>
        )}
      </div>
    </div>
  );
}
