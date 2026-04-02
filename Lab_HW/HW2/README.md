Hw2
	- Implement logout
	- Write role dropdown to the registration function
	- Implement a HREF in the dashboard visible only to the role: admin
	- Implement page accessible only to role: admin from HREF in ex 3
Users
	Id
	Usernmae/email
	Password
	Role

## How to Run

1. Ensure Docker and Docker Compose are installed.
2. In the `HW2` directory, start the infrastructure and application by running:
   ```bash
   docker-compose up -d --build
   ```
3. Once built and running, open your browser and navigate to:
   **http://localhost:5000**

*(Note: The database auto-initializes. You can register your own admin account directly through the registration UI).*