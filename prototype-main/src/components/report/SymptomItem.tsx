
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { X, ChevronDown } from "lucide-react";

interface SymptomItemProps {
  symptom: string;
  onRemove: () => void;
  onSeverityChange: (severity: string) => void;
}

export const SymptomItem = ({ symptom, onRemove, onSeverityChange }: SymptomItemProps) => {
  const [severity, setSeverity] = useState<string>("Low");
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const handleSeverityChange = (newSeverity: string) => {
    setSeverity(newSeverity);
    onSeverityChange(newSeverity);
    setIsOpen(false);
  };

  const getSeverityColor = () => {
    switch (severity) {
      case "Low":
        return "bg-green-500 hover:bg-green-600";
      case "Medium":
        return "bg-yellow-400 hover:bg-yellow-500";
      case "High":
        return "bg-red-500 hover:bg-red-600";
      default:
        return "bg-green-500 hover:bg-green-600";
    }
  };

  return (
    <div className="flex items-center justify-between bg-white p-3 rounded-md shadow-sm mb-2 border border-gray-200">
      <div className="font-medium">{symptom}</div>
      <div className="flex items-center gap-2">
        <div className="relative">
          <Button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className={`${getSeverityColor()} text-white text-xs h-8 flex items-center`}
          >
            {severity} <ChevronDown className="ml-1 h-3 w-3" />
          </Button>
          
          {isOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white shadow-lg rounded-md border border-gray-200 z-10">
              <div className="py-1">
                <button
                  type="button"
                  className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 text-green-600"
                  onClick={() => handleSeverityChange("Low")}
                >
                  Low
                </button>
                <button
                  type="button"
                  className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 text-yellow-500"
                  onClick={() => handleSeverityChange("Medium")}
                >
                  Medium
                </button>
                <button
                  type="button"
                  className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 text-red-600"
                  onClick={() => handleSeverityChange("High")}
                >
                  High
                </button>
              </div>
            </div>
          )}
        </div>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          onClick={onRemove}
          className="h-8 w-8 p-0"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};
