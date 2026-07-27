import { useEffect, useState } from "react";
import { getUsers } from "../services/user";

function Users() {
    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadUsers();
    }, []);

    const loadUsers = async () => {
        try {
            const data = await getUsers();
            setUsers(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <h2 style={{ padding: 30 }}>Loading users...</h2>;
    }

    return (
        <div style={{ padding: 30 }}>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: 20,
                }}
            >
                <h1>Users</h1>

                <button
                    style={{
                        padding: "10px 18px",
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        borderRadius: 8,
                        cursor: "pointer",
                    }}
                >
                    + Invite User
                </button>
            </div>

            <table
                style={{
                    width: "100%",
                    borderCollapse: "collapse",
                }}
            >
                <thead>
                    <tr
                        style={{
                            background: "#f3f4f6",
                        }}
                    >
                        <th style={{ padding: 12 }}>Username</th>
                        <th>Email</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    {users.map((user) => (
                        <tr
                            key={user.user_id}
                            style={{
                                borderBottom: "1px solid #ddd",
                            }}
                        >
                            <td style={{ padding: 12 }}>
                                {user.username}
                            </td>

                            <td>{user.email}</td>

                            <td>{user.status}</td>

                            <td>
                                <button>Edit</button>{" "}
                                <button>Disable</button>{" "}
                                <button>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Users;