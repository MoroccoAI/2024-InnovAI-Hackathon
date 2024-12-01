import { Col, Row } from "reactstrap";
import FlowChart from "../../dashboard/FlowChart";
import Feeds from "../../../components/dashboard/Feeds";
import EventHistory from "../../dashboard/EventHistory";
import TopCards from "../../../components/dashboard/TopCards";




const Starter = () => {
  return (
    <div>
      {/***Top Cards***/}
      <Row>
  <Col sm="6" lg="3">
    <TopCards
      bg="bg-light-success text-success"
      title="Water Consumption"
      subtitle="Real-time Flow Data"
      earning="30L"
      icon="bi bi-droplet"
    />
  </Col>
  <Col sm="6" lg="3">
    <TopCards
      bg="bg-light-danger text-danger"
      title="Leak Detection"
      subtitle="Detected Leaks"
      earning="100 Dh saved"
      icon="bi bi-currency-dollar"
    />
  </Col>
  <Col sm="6" lg="3">
    <TopCards
      bg="bg-light-warning text-warning"
      title="Flow Rate Analytics"
      subtitle="Flow Insights"
      earning="10L/hour"
      icon="bi bi-speedometer2"
    />
  </Col>
  <Col sm="6" lg="3">
    <TopCards
      bg="bg-light-info text-info"
      title="Water Usage"
      subtitle="Weekly Water Consumption"
      earning="50 L/week"
      icon="bi bi-calendar-week"
    />
  </Col>
</Row>

      {/***Feed***/}
      <Row>
        <Col sm="6" lg="6" xl="7" xxl="8">
          <FlowChart />
        </Col>
        <Col sm="6" lg="6" xl="5" xxl="4">
          <Feeds />
        </Col>
      </Row>
      {/***Table ***/}
      <Row>
        <Col lg="12">
          <EventHistory />
        </Col>
      </Row>
    </div>
  );
};

export default Starter;
