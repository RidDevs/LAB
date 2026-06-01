import UserList from "./userlist";

function App() {
  const users = [
    { id: 1, name: "John" },
    { id: 2, name: "Alice" },
    { id: 3, name: "Bob" }
  ];

  return (
    <>
      <h2>User List</h2>
      <UserList users={users} />
    </>
  );
}

export default App;