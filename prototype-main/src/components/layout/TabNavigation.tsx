
import { useState } from "react";
import { cn } from "@/lib/utils";
import { useNavigate, useLocation } from "react-router-dom";
import { LayoutDashboard, FileInput, User } from "lucide-react";

interface TabItem {
  id: string;
  label: string;
  path: string;
  icon: React.ReactNode;
}

export function TabNavigation() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const tabs: TabItem[] = [
    {
      id: "dashboard",
      label: "Dashboard",
      path: "/",
      icon: <LayoutDashboard className="h-5 w-5" />,
    },
    {
      id: "report",
      label: "Self Report",
      path: "/report",
      icon: <FileInput className="h-5 w-5" />,
    },
    {
      id: "profile",
      label: "User Profile",
      path: "/profile",
      icon: <User className="h-5 w-5" />,
    },
  ];

  const handleTabChange = (path: string) => {
    navigate(path);
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg py-2 px-4 z-50 md:top-0 md:bottom-auto md:border-t-0 md:border-b">
      <div className="container max-w-4xl mx-auto">
        <div className="flex justify-between items-center">
          <div className="md:flex items-center">
            <h1 className="text-xl font-bold text-health-blue hidden md:block">
              HealthRadar
            </h1>
          </div>
          <div className="flex justify-between w-full md:w-auto md:ml-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleTabChange(tab.path)}
                className={cn(
                  "flex flex-col md:flex-row items-center px-4 py-2 rounded-md transition-colors",
                  location.pathname === tab.path
                    ? "text-health-blue font-medium"
                    : "text-gray-500 hover:text-health-blue"
                )}
              >
                <span className="md:mr-2">{tab.icon}</span>
                <span className="text-xs md:text-sm">{tab.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
