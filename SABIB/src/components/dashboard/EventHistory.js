import React from "react";
import { Card, CardBody, CardTitle, CardSubtitle, Table } from "reactstrap";

const eventHistory = [
  {
    event: "High Water Flow Detected",
    category: "Alert",
    timestamp: "2024-04-20 09:30 AM",
    badgeColor: "bg-danger",
  },
  {
    event: "Low Water Pressure",
    category: "Info",
    timestamp: "2024-04-18 02:15 PM",
    badgeColor: "bg-info",
  },
  {
    event: "High Water Usage recorded",
    category: "Info",
    timestamp: "2024-04-15 10:00 AM",
    badgeColor: "bg-info",
  },
  {
    event: "Leak Detected in Bathroom",
    category: "Alert",
    timestamp: "2024-04-10 11:45 AM",
    badgeColor: "bg-danger",
  },
];

const EventHistory = () => {
  return (
    <div>
      <Card>
        <CardBody>
          <CardTitle tag="h5">Alert & Event History</CardTitle>

          <Table className="no-wrap mt-3 align-middle" responsive borderless>
            <thead>
              <tr>
                <th>Event</th>
                <th>Category</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {eventHistory.map((event, index) => (
                <tr key={index} className="border-top">
                  <td>{event.event}</td>
                  <td>
                    <span className={`badge ${event.badgeColor}`}>{event.category}</span>
                  </td>
                  <td>{event.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardBody>
      </Card>
    </div>
  );
};

export default EventHistory;
