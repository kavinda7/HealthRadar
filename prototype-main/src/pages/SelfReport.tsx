
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { MapPin } from "lucide-react";
import { SymptomItem } from "@/components/report/SymptomItem";

interface SymptomReport {
  symptom: string;
  severity: string;
}

export default function SelfReport() {
  const [selectedSymptoms, setSelectedSymptoms] = useState<SymptomReport[]>([]);
  const [symptomToAdd, setSymptomToAdd] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [locationPermission, setLocationPermission] = useState<boolean | null>(null);
  const navigate = useNavigate();

  const symptoms = [
    "Fever",
    "Cough",
    "Nasal Congestion",
    "Sore Throat",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Headache",
    "Skin Rash",
  ];

  const requestLocationPermission = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        () => {
          setLocationPermission(true);
          toast.success("Location access granted");
        },
        (error) => {
          console.error("Location error:", error);
          setLocationPermission(false);
          toast.error("Location access denied. You can still submit a report, but it won't be mapped accurately.");
        }
      );
    } else {
      setLocationPermission(false);
      toast.error("Geolocation is not supported by your browser");
    }
  };

  const handleAddSymptom = () => {
    if (!symptomToAdd) return;
    
    // Check if symptom is already added
    if (selectedSymptoms.some(item => item.symptom === symptomToAdd)) {
      toast.error(`${symptomToAdd} is already added`);
      return;
    }
    
    setSelectedSymptoms([
      ...selectedSymptoms, 
      { symptom: symptomToAdd, severity: "Low" }
    ]);
    setSymptomToAdd("");
  };

  const handleRemoveSymptom = (index: number) => {
    const newSymptoms = [...selectedSymptoms];
    newSymptoms.splice(index, 1);
    setSelectedSymptoms(newSymptoms);
  };

  const handleUpdateSeverity = (index: number, severity: string) => {
    const newSymptoms = [...selectedSymptoms];
    newSymptoms[index].severity = severity;
    setSelectedSymptoms(newSymptoms);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (selectedSymptoms.length === 0) {
      toast.error("Please add at least one symptom");
      return;
    }
    
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      toast.success("Thank you for your symptom report!");
      console.log("Submitted symptoms:", selectedSymptoms);
      setIsSubmitting(false);
      navigate("/", { replace: true });
    }, 1500);
  };

  return (
    <div className="container max-w-md mx-auto pt-4 pb-24 md:pt-24 md:pb-4 px-4">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-center mb-6 text-health-blue">Report Your Symptoms</h2>

        {locationPermission === null ? (
          <div className="text-center mb-8">
            <p className="mb-4 text-gray-700">
              To accurately map health data, HealthRadar needs your location permission.
            </p>
            <Button
              onClick={requestLocationPermission}
              className="bg-health-blue hover:bg-health-blue-light text-white flex items-center gap-2"
            >
              <MapPin size={18} />
              Allow Location Access
            </Button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            {!locationPermission && (
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
                <p className="text-sm text-yellow-700">
                  Location access is denied. Your report will be submitted without exact location data.
                </p>
              </div>
            )}
            
            <div>
              <label htmlFor="symptom" className="block text-sm font-medium text-gray-700 mb-1">
                Add Symptoms
              </label>
              <div className="flex gap-2">
                <select
                  id="symptom"
                  value={symptomToAdd}
                  onChange={(e) => setSymptomToAdd(e.target.value)}
                  className="flex-1 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-health-blue"
                >
                  <option value="">Select symptom</option>
                  {symptoms.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
                <Button
                  type="button"
                  onClick={handleAddSymptom}
                  disabled={!symptomToAdd}
                  className="bg-health-blue hover:bg-health-blue-light text-white"
                >
                  Add
                </Button>
              </div>
            </div>

            {selectedSymptoms.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Selected Symptoms
                </label>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {selectedSymptoms.map((item, index) => (
                    <SymptomItem
                      key={item.symptom}
                      symptom={item.symptom}
                      onRemove={() => handleRemoveSymptom(index)}
                      onSeverityChange={(severity) => handleUpdateSeverity(index, severity)}
                    />
                  ))}
                </div>
              </div>
            )}

            <div className="pt-4">
              <Button
                type="submit"
                className="w-full bg-health-blue hover:bg-health-blue-light text-white"
                disabled={isSubmitting || selectedSymptoms.length === 0}
              >
                {isSubmitting ? "Submitting..." : "Submit Report"}
              </Button>
            </div>
          </form>
        )}

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>
            Your health data helps us track and prevent outbreaks in your community.
            All reports are anonymous.
          </p>
        </div>
      </div>
    </div>
  );
}
