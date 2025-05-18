
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Newspaper, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";

interface NewsItem {
  id: string;
  title: string;
  source: string;
  date: string;
  url: string;
}

interface NewsWidgetProps {
  diseaseType: string;
  location: string;
}

export const NewsWidget = ({ diseaseType, location }: NewsWidgetProps) => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchNews = async () => {
      setIsLoading(true);
      
      // In a real application, this would fetch from a news API
      // For this prototype, we'll simulate fetching news with a timeout
      setTimeout(() => {
        // Generate mock news data based on the disease type and location
        const mockNews: NewsItem[] = [
          {
            id: "1",
            title: `WHO reports on ${diseaseType} cases rising in Northern Europe`,
            source: "World Health Organization",
            date: "2 days ago",
            url: "https://www.who.int/health-topics/disease-outbreaks",
          },
          {
            id: "2",
            title: `${location} health authorities issue ${diseaseType} advisory`,
            source: "Local Health Department",
            date: "5 days ago",
            url: "https://www.who.int/emergencies/disease-outbreak-news",
          },
          {
            id: "3",
            title: `New prevention measures for ${diseaseType} announced`,
            source: "CDC",
            date: "1 week ago",
            url: "https://www.cdc.gov/outbreaks/",
          },
        ];
        
        setNews(mockNews);
        setIsLoading(false);
      }, 800);
    };
    
    fetchNews();
  }, [diseaseType, location]);

  return (
    <Card className="mt-4">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-md font-medium flex items-center gap-2">
          <Newspaper className="h-5 w-5 text-health-blue" />
          Recent Outbreak News
        </CardTitle>
        <Badge variant="outline" className="text-xs bg-health-blue text-white">
          WHO Sourced
        </Badge>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-2">
            <div className="h-5 bg-gray-200 rounded animate-pulse w-full"></div>
            <div className="h-5 bg-gray-200 rounded animate-pulse w-3/4"></div>
            <div className="h-5 bg-gray-200 rounded animate-pulse w-5/6"></div>
          </div>
        ) : (
          <ul className="space-y-3">
            {news.map((item) => (
              <li key={item.id} className="border-b border-gray-100 pb-2 last:border-0">
                <a 
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-sm hover:text-health-blue transition-colors"
                >
                  <div className="font-medium">{item.title}</div>
                  <div className="text-xs flex justify-between mt-1 text-gray-500">
                    <span>{item.source}</span>
                    <span>{item.date}</span>
                  </div>
                </a>
              </li>
            ))}
          </ul>
        )}
        
        <Button variant="outline" size="sm" className="w-full mt-3 text-xs" asChild>
          <a 
            href="https://www.who.int/emergencies/disease-outbreak-news" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center justify-center"
          >
            View All WHO Outbreak News
            <ExternalLink className="ml-1 h-3 w-3" />
          </a>
        </Button>
      </CardContent>
    </Card>
  );
};
