
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to the dashboard
    navigate("/", { replace: true });
  }, [navigate]);

  // Loading screen while redirecting
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4 text-health-blue">Loading HealthRadar...</h1>
      </div>
    </div>
  );
};

export default Index;
