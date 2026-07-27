import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signup } from "../services/auth";

function Signup() {
    const navigate = useNavigate();

    const [organizationName, setOrganizationName] = useState("");
    const [organizationSlug, setOrganizationSlug] = useState("");
    const [organizationTier] = useState("free");
    const [displayName, setDisplayName] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSignup = async () => {
        console.log("Button clicked");

        try {
            const response = await signup({
                organization_name: organizationName,
                organization_slug: organizationSlug,
                organization_tier: organizationTier,
                display_name: displayName,
                username,
                email,
                password,
            });

            localStorage.setItem(
                "access_token",
                response.access_token
            );

            alert("Signup Successful!");

            console.log(response);

            // Navigate to Dashboard
            navigate("/dashboard");
        } catch (error: any) {
            console.error(error);

            if (error.response) {
                console.log("Status:", error.response.status);
                console.log(error.response.data);
                alert(
                    error.response.data.detail ??
                    JSON.stringify(error.response.data)
                );
            } else {
                alert(error.message);
            }
        }
    };

    return (
        <div
            style={{
                width: "430px",
                margin: "60px auto",
                padding: "30px",
                borderRadius: "12px",
                boxShadow: "0 0 15px rgba(0,0,0,0.15)",
                display: "flex",
                flexDirection: "column",
                gap: "12px",
                background: "white",
            }}
        >
            <h2 style={{ textAlign: "center" }}>
                Create Organization
            </h2>

            <input
                placeholder="Organization Name"
                value={organizationName}
                onChange={(e) =>
                    setOrganizationName(e.target.value)
                }
            />

            <input
                placeholder="Organization Slug"
                value={organizationSlug}
                onChange={(e) =>
                    setOrganizationSlug(e.target.value)
                }
            />

            <input
                placeholder="Display Name"
                value={displayName}
                onChange={(e) =>
                    setDisplayName(e.target.value)
                }
            />

            <input
                placeholder="Username"
                value={username}
                onChange={(e) =>
                    setUsername(e.target.value)
                }
            />

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
            />

            <button
                onClick={handleSignup}
                style={{
                    padding: "12px",
                    border: "none",
                    borderRadius: "8px",
                    background: "#2563eb",
                    color: "white",
                    fontWeight: "bold",
                    cursor: "pointer",
                }}
            >
                Create Organization
            </button>
        </div>
    );
}

export default Signup;