import React, { useState, useEffect } from 'react';
import { Card, CardBody, CardSubtitle, CardTitle } from 'reactstrap';
import Chart from 'react-apexcharts';
import axios from 'axios';

const FlowChart = () => {
  const [chartData, setChartData] = useState({ series: [], options: {} });

  useEffect(() => {
    const fetchData = async () => {
      const apiKey = 'FSVBSPI6O9L9GDJC';
      const channelId = 2450142;
      const fieldId = 1;
      const results = 8; // Adjust the number of results as needed

      try {
        const response = await axios.get(
          `https://api.thingspeak.com/channels/${channelId}/fields/${fieldId}.json?api_key=${apiKey}&results=${results}`
        );

        const { feeds } = response.data;
        const dataSeries = feeds.map((feed) => parseInt(feed.field1, 10)); // Assuming field1 contains data you want to plot

        const updatedChartData = {
          series: [
            {
              name: 'ThingSpeak Data',
              data: dataSeries,
            },
          ],
          options: {
            chart: {
              type: 'area',
            },
            dataLabels: {
              enabled: false,
            },
            grid: {
              strokeDashArray: 3,
            },
            stroke: {
              curve: 'smooth',
              width: 1,
            },
            xaxis: {
              categories: feeds.map((feed) => feed.created_at), // Assuming created_at contains x-axis labels
            },
          },
        };

        setChartData(updatedChartData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []); // Run only once on component mount

  return (
    <Card>
      <CardBody>
        <CardTitle tag="h5">Flow Rate</CardTitle>
        <CardSubtitle className="text-muted" tag="h6">
        Flow Rate Overview
        </CardSubtitle>
        <Chart
          type="area"
          width="100%"
          height="390"
          options={chartData.options}
          series={chartData.series}
        />
      </CardBody>
    </Card>
  );
};

export default FlowChart;
