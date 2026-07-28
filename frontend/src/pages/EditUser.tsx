import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getUser, updateUser } from "../services/user";

function EditUser() {
    const { userId } = useParams();

    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);

    const [saving, setSaving] = useState(false);

    const [form, setForm] = useState({
        username: "",
        email: "",
    });

    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            const data = await getUser(userId!);

            setForm({
                username: data.username,
                email: data.email,
            });
        } catch (err) {
            console.error(err);
            alert("Unable to load user.");
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (
        e: React.FormEvent
    ) => {
        e.preventDefault();

        try {
            setSaving(true);

            await updateUser(userId!, form);

            alert("User updated successfully.");

            navigate("/users");
        } catch (err: any) {
            console.error(err);

            alert(
                err.response?.data?.detail ??
                    "Unable to update user."
            );
        } finally {
            setSaving(false);
        }
    };

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
                maxWidth: 600,
                margin: "50px auto",
                fontFamily: "Arial",
            }}
        >
            <h1>Edit User</h1>

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 20 }}>
                    <label>Username</label>

                    <input
                        name="username"
                        value={form.username}
                        onChange={handleChange}
                        required
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <div style={{ marginBottom: 20 }}>
                    <label>Email</label>

                    <input
                        type="email"
                        name="email"
                        value={form.email}
                        onChange={handleChange}
                        required
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={saving}
                    style={{
                        padding: "12px 24px",
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        borderRadius: 8,
                        cursor: "pointer",
                    }}
                >
                    {saving ? "Updating..." : "Update User"}
                </button>
            </form>
        </div>
    );
}

export default EditUser;