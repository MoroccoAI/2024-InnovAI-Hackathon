import React from "react";
import {
  Card,
  CardBody,
  CardTitle,
  ListGroup,
  CardSubtitle,
  ListGroupItem,
  Button,
} from "reactstrap";

const FeedData = [
  {
    title: "Flow Rate Alert",
    icon: "bi bi-speedometer2",
    color: "danger",
    date: "6 minutes ago",
  },
  {
    title: "Low Water Pressure Detected",
    icon: "bi bi-bar-chart-line",
    color: "warning",
    date: "12 minutes ago",
  },
  {
    title: "High Water Usage Recorded",
    icon: "bi bi-droplet",
    color: "info",
    date: "18 minutes ago",
  },
  {
    title: "Leak Detected",
    icon: "bi bi-exclamation-triangle",
    color: "danger",
    date: "25 minutes ago",
  },
];

const Feeds = () => {
  return (
    <Card>
      <CardBody>
        <CardTitle tag="h5">System Alerts</CardTitle>
        <CardSubtitle className="mb-2 text-muted" tag="h6">
          Real-time Notifications
        </CardSubtitle>
        <ListGroup flush className="mt-4">
          {FeedData.map((feed, index) => (
            <ListGroupItem
              key={index}
              action
              href="/"
              tag="a"
              className="d-flex align-items-center p-3 border-0"
            >
              <Button
                className="rounded-circle me-3"
                size="sm"
                color={feed.color}
              >
                <i className={feed.icon}></i>
              </Button>
              {feed.title}
              <small className="ms-auto text-muted text-small">
                {feed.date}
              </small>
            </ListGroupItem>
          ))}
        </ListGroup>
      </CardBody>
    </Card>
  );
};

export default Feeds;
