import { useState, useEffect } from "react";
import { Bar, Pie } from "react-chartjs-2";
import Chart from "chart.js/auto";
import { useParams, useOutletContext } from "react-router-dom";

export default function AgentStats() {
    const { agent_id } = useParams();
    const { data } = useOutletContext();
    const audio = data.find((audio) => audio.agent_id == agent_id);

    console.log(agent_id);
    console.log(audio);

    return <div>sss</div>
}
