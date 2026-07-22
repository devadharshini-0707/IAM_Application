import { useState } from "react";
import { signup } from "../services/auth";

function Signup() {
    const [organizationName, setOrganizationName] = useState("");
    const [organizationSlug, setOrganizationSlug] = useState("");
    const [organizationTier, setOrganizationTier] = useState("free");
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
        }catch (error: any) {
    console.error(error);

            if (error.response) {
                console.log("Status:", error.response.status);
                console.log("Data:", error.response.data);
                alert(JSON.stringify(error.response.data));
            } else {
                alert(error.message);
            }
        }
    };

    return (
        <div
            style={{
                width: "420px",
                margin: "50px auto",
                display: "flex",
                flexDirection: "column",
                gap: "12px",
            }}
        >
            <h1>IAM Signup</h1>

            <input
                placeholder="Organization Name"
                value={organizationName}
                onChange={(e) => setOrganizationName(e.target.value)}
            />

            <input
                placeholder="Organization Slug"
                value={organizationSlug}
                onChange={(e) => setOrganizationSlug(e.target.value)}
            />

            <input
                placeholder="Display Name"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
            />

            <input
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={handleSignup}>
                Create Organization
            </button>
        </div>
    );
}

export default Signup;