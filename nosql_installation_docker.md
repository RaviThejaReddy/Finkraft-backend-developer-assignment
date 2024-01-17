1. **Create a Docker Compose File:**
   Create a `docker-compose.yml` file in your project directory to define the MongoDB service.

   ```yaml
   version: '3'

   services:
     nosql_db:
       image: mongo:latest
       ports:
         - "27017:27017"
   ```

   This configuration uses the official MongoDB Docker image and maps port 27017 on your host machine to the MongoDB container.

2. **Run Docker Compose:**
   Open a terminal and run the following command to start the MongoDB service:

   ```bash
   docker-compose up -d
   ```

   The `-d` flag runs the containers in the background.

3. **Verify MongoDB Container:**
   You can check if the MongoDB container is running using:

   ```bash
   docker ps
   ```

   You should see a container named `projectfolder_name_nosql_db` (the prefix is based on your project folder name).

4. **Update Flask App Configuration:**
   Ensure that your Flask app's `MONGO_URI` is correctly set in the environment variables or configuration. It should point to the MongoDB instance and include the database name:

   ```
   MONGO_URI=mongodb://localhost:27017/product_catalog
   ```