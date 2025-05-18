
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Award, Calendar, CheckCircle, LogOut } from "lucide-react";

export default function UserProfile() {
  const [user] = useState({
    name: "Jane Doe",
    age: 34,
    profilePicture: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=250&h=250",
    memberSince: "May 2023",
    reportsSubmitted: 47,
    outbreaksContributed: 3
  });
  
  const [badges] = useState([
    {
      id: 1,
      name: "First to Report",
      description: "First to Report in Your Area",
      icon: <CheckCircle className="h-5 w-5" />,
      earned: true
    },
    {
      id: 2,
      name: "100 Reports",
      description: "100 Symptoms Reported – One Potential Life Saved",
      icon: <Award className="h-5 w-5" />,
      earned: false
    },
    {
      id: 3,
      name: "7-Day Streak",
      description: "7-Day Streak Reporter",
      icon: <Calendar className="h-5 w-5" />,
      earned: true
    }
  ]);

  const [activities] = useState([
    {
      id: 1,
      type: "report",
      description: "Reported Fever with Medium severity",
      date: "3 days ago"
    },
    {
      id: 2,
      type: "badge",
      description: "Earned 7-Day Streak Reporter badge",
      date: "1 week ago"
    },
    {
      id: 3,
      type: "alert",
      description: "Triggered Influenza risk alert in your area",
      date: "2 weeks ago"
    },
    {
      id: 4,
      type: "report",
      description: "Reported Cough with Low severity",
      date: "2 weeks ago"
    }
  ]);

  const handleLogout = () => {
    toast.success("You have been logged out");
    // In a real app, this would handle actual logout logic
  };

  return (
    <div className="container max-w-md mx-auto pt-4 pb-24 md:pt-24 md:pb-4 px-4">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        {/* Profile Header */}
        <div className="bg-health-blue text-white p-6 text-center">
          <div className="mb-4 flex justify-center">
            <img
              src={user.profilePicture}
              alt={user.name}
              className="w-24 h-24 rounded-full border-4 border-white object-cover"
            />
          </div>
          <h2 className="text-2xl font-bold">{user.name}</h2>
          <p className="text-health-blue-light">Age: {user.age}</p>
          <p className="text-sm mt-1">Member since: {user.memberSince}</p>
        </div>

        {/* Badges Section */}
        <div className="p-6 border-b">
          <h3 className="text-lg font-bold mb-4 flex items-center">
            <Award className="mr-2 h-5 w-5 text-health-blue" />
            Your Badges
          </h3>
          <div className="grid grid-cols-1 gap-3">
            {badges.map((badge) => (
              <div key={badge.id} className="flex items-center">
                <div className={`p-2 rounded-full mr-3 ${badge.earned ? 'bg-health-blue text-white' : 'bg-gray-200 text-gray-500'}`}>
                  {badge.icon}
                </div>
                <div>
                  <h4 className="font-medium">{badge.name}</h4>
                  <p className="text-sm text-gray-600">{badge.description}</p>
                  {!badge.earned && (
                    <Badge variant="outline" className="mt-1 text-xs">In Progress</Badge>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Impact Section */}
        <div className="p-6 border-b">
          <h3 className="text-lg font-bold mb-4">Your Impact</h3>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-gray-50 p-4 rounded-lg text-center">
              <span className="block text-2xl font-bold text-health-blue">{user.reportsSubmitted}</span>
              <span className="text-sm text-gray-600">Reports Submitted</span>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg text-center">
              <span className="block text-2xl font-bold text-health-blue">{user.outbreaksContributed}</span>
              <span className="text-sm text-gray-600">Outbreaks Contributed</span>
            </div>
          </div>
          <p className="text-sm text-gray-600">
            Your reports have helped health authorities track and respond to threats in your community. Thank you!
          </p>
        </div>

        {/* Recent Activity */}
        <div className="p-6 border-b">
          <h3 className="text-lg font-bold mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {activities.map((activity) => (
              <div key={activity.id} className="flex items-start">
                <div className="w-2 h-2 mt-2 rounded-full bg-health-blue mr-3"></div>
                <div>
                  <p className="text-gray-800">{activity.description}</p>
                  <p className="text-xs text-gray-500">{activity.date}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Logout Button */}
        <div className="p-6">
          <Button 
            onClick={handleLogout} 
            variant="destructive"
            className="w-full flex items-center justify-center gap-2"
          >
            <LogOut size={16} />
            Logout
          </Button>
        </div>
      </div>
    </div>
  );
}
