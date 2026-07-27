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
                    "TOKEN FROM LOCALSTORAGE:",
                    localStorage.getItem("access_token")
                );
                console.log("=================================");

                const data = await getCurrentUser();

                console.log("USER DATA:", data);

                setUser(data);
            } catch (err: any) {
                console.error("GET CURRENT USER FAILED");
                console.error(err);

                if (err.response) {
                    console.log("STATUS:", err.response.status);
                    console.log("DATA:", err.response.data);
                }

                // DON'T remove the token yet.
                // We want to find the real error first.

                // localStorage.removeItem("access_token");
                // navigate("/login");
            } finally {
                setLoading(false);
            }
        };

        loadUser();
    }, []);

    if (loading) {
        return (
            <div style={{ padding: "40px" }}>
                <h2>Loading...</h2>
            </div>
        );
    }

    return (
        <div
            style={{
                padding: "40px",
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
                <div
                    style={{
                        border: "1px solid gray",
                        padding: "20px",
                        borderRadius: "10px",
                    }}
                >
                    <h3>Users</h3>
                    <p>Manage organization users</p>
                </div>

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
