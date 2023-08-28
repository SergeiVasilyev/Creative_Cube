<script>
    let username = "";
    let password = "";
  
    async function login() {
      const response = await fetch("http://127.0.0.1:8000/api-auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });
  
      if (response.ok) {
        // Redirect or perform other actions on successful login
      } else {
        // Handle login error
      }
    }
  </script>
  
  <main>
    <h1>Login</h1>
    <input type="text" bind:value={username} placeholder="Username" />
    <input type="password" bind:value={password} placeholder="Password" />
    <button on:click={login}>Login</button>
  </main>
  
  <style>
    /* Your styles here */
  </style>