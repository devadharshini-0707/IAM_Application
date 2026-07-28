import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser } from "../services/user";

function Dashboard() {
    const navigate = useNavigate();

    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadUser = async () => {
            try {
                console.log("=================================");
                console.log(
                    "TOKEN:",
                    localStorage.getItem("access_token")
                );
                console.log("=================================");

                const data = await getCurrentUser();

                console.log("USER:", data);

                setUser(data);
            } catch (err: any) {
                console.error(err);

                if (err.response) {
                    console.log(err.response.status);
                    console.log(err.response.data);
                }
            } finally {
                setLoading(false);
            }
        };

        loadUser();
    }, []);

    if (loading) {
        return (
            <div style={{ padding: 40 }}>
                <h2>Loading...</h2>
            </div>
        );
    }

    return (
        <div
            style={{
                padding: 40,
                fontFamily: "Arial",
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                }}
            >
                <div>
                    <h1>IAM Dashboard</h1>

                    {user ? (
                        <>
                            <h3>Welcome, {user.username}</h3>
                            <p>{user.email}</p>
                        </>
                    ) : (
                        <h3>No user loaded</h3>
                    )}
                </div>

                <button
                    onClick={() => {
                        localStorage.removeItem("access_token");
                        navigate("/login");
                    }}
                    style={{
                        padding: "10px 18px",
                        background: "#ef4444",
                        color: "white",
                        border: "none",
                        borderRadius: "8px",
                        cursor: "pointer",
                    }}
                >
                    Logout
                </button>
            </div>

            <hr />

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(3,1fr)",
                    gap: "20px",
                    marginTop: "30px",
                }}
            >
                {/* USERS */}
                <div
                    onClick={() => navigate("/users")}
                    style={{
                        border: "1px solid gray",
                        padding: "20px",
                        borderRadius: "10px",
                        cursor: "pointer",
                        transition: "0.2s",
                    }}
                >
                    <h3>Users</h3>
                    <p>Manage organization users</p>
                </div>

                {/* ROLES */}
                <div
                    style={{
                        border: "1px solid gray",
                        padding: "20px",
                        borderRadius: "10px",
                    }}
                >
                    <h3>Roles</h3>
                    <p>Create and assign roles</p>
                </div>

                {/* GROUPS */}
                <div
                    style={{
                        border: "1px solid gray",
                        padding: "20px",
                        borderRadius: "10px",
                    }}
                >
                    <h3>Groups</h3>
                    <p>Manage user groups</p>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;