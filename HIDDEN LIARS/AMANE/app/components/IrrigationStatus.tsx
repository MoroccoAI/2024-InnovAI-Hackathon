import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTriangle, CheckCircle, Droplet, ShieldOff } from "lucide-react";

// Define the type for the card configurations
type CardConfig = {
  key: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  iconColor: string;
  activeClassName: string;
};

// Define the props type
type IrrigationStatusCardsProps = {
  modelResponse: string;
};

const IrrigationStatusCards: React.FC<IrrigationStatusCardsProps> = ({ modelResponse }) => {
  // Predefined card configurations
  const cardConfigs: CardConfig[] = [
    {
      key: "ALERT",
      label: "Alert",
      icon: AlertTriangle,
      iconColor: "text-red-500",
      activeClassName: "border-red-500 bg-red-50"
    },
    {
      key: "No adjustment",
      label: "No Adjustment",
      icon: CheckCircle,
      iconColor: "text-green-500",
      activeClassName: "border-green-500 bg-green-50"
    },
    {
      key: "Irrigation ON",
      label: "Irrigation On",
      icon: Droplet,
      iconColor: "text-blue-500",
      activeClassName: "border-blue-500 bg-blue-50"
    },
    {
      key: "Irrigation OFF",
      label: "Irrigation Off",
      icon: ShieldOff,
      iconColor: "text-gray-500",
      activeClassName: "border-gray-500 bg-gray-50"
    }
  ];

  return (
    <div className="grid grid-cols-2 gap-4">
      {cardConfigs.map((config) => (
        <Card
          key={config.key}
          className={`max-w-xs border-2 ${modelResponse === config.key ? config.activeClassName : "border-gray-300"}`}
        >
          <CardHeader>
            <div className="flex items-center">
              <config.icon className={`${config.iconColor} mr-2`} />
              <CardTitle>{config.label}</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {modelResponse === config.key ? "Active" : "Inactive"}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default IrrigationStatusCards;
