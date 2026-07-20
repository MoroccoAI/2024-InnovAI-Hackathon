import { createBrowserRouter, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import HomeUI from "./pages/home/home";
import ManagerUI from "./pages/manager/manager";
import AgentUI from "./pages/agent/agent";
import SideBar from "./components/sidebar/sidebar";
import data from "./data";
import AudioDetail from "./pages/audioDetail/audioDetail";
import AgentStats from "./pages/manager/agent_stats";

function App() {
    const location = useLocation();
    const navigate = useNavigate();
    const [currentPage, setCurrentPage] = useState("");

    useEffect(() => {
        setCurrentPage(location.pathname);
    }, [location]);

    const isNotHome = currentPage.includes("manager") || currentPage.includes("agent");

    function navigateToHome() {
        navigate("/");
    }

    return (
        <>
            {/* <div className="">
                {isNotHome && <SideBar navigateToHome={navigateToHome} currentPage={currentPage} data={data} />}
                <div className="home-button" onClick={navigateToHome}>
                    Home
                </div>
                <Outlet context={{ data }} />
            </div> */}
            <Outlet context={{ data }} />
            {/* <Outlet /> */}
        </>
    );
}

export const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                path: "",
                element: <HomeUI />,
            },
            {
                path: "agent",
                element: <AgentUI />,
                children: [
                    {
                        path: "",
                        element: <AgentUI />,
                    },
                    {
                        path: ":id",
                        element: <AgentUI />,
                    },
                ],
            },
            {
                path: "manager",
                element: <ManagerUI />,
                children: [
                    {
                        path: "",
                        element: <AgentUI />,
                    },
                    {
                        path: ":agent_id",
                        element: <AgentStats />,
                    },
                ],
            },
            {
                path: ":client_id",
                element: <AudioDetail />,
            },
        ],
    },
]);
