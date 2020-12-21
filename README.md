# CARPET

CARPET is the main tool of the PrYVeCT framework, a *privacy-yet-verifiable* contact tracing system developed by IMT School for Advanced Studies in Lucca.

#### Execution of the tool

- Download the tool

- Open two terminal window

- Type the following commands in the first one
  
  ```bash
  cd CARPET/Server
  docker-compose up
  ```

        Doing this the CARPET server and its db start

- Type the following commands in the second one
  
  ```bash
  cd CARPET/Client
  docker build .
  docker run --network host [container_name]
  ```

        Doing this the CARPET client starts and the Oblivious Transfer protocol is executed
