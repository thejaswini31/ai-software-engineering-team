import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";


function Dashboard() {

    const [data, setData] = useState({});

    useEffect(() => {

        loadDashboard();

    }, []);

    const loadDashboard = async () => {

        try {

            const response =
                await api.get("/dashboard");

            setData(response.data);

        } catch (error) {

            console.log(error);
        }
    };

    const logout = () => {

        localStorage.removeItem("token");

        window.location.href = "/";
    };

    const navigate = useNavigate();

    return (

        <div>

            <h1>
                AI Software Engineering Team
            </h1>

            <h2>
                Dashboard
            </h2>

            <h3>
                Total Users: {data.total_users}
            </h3>

            <h3>
                Total Chats: {data.total_chats}
            </h3>

            <br />

            <button onClick={logout}>
                Logout
            </button>

            <button
                onClick={() =>
                    navigate("/upload")
                }
            >
                Upload PDF
            </button>

            <button
                onClick={() =>
                    navigate("/chat")
                }
            >
                Chat With PDF
            </button>

        </div>
    );
}

export default Dashboard;