# Flapper Boarding Pass
Microservice that generates Flapper boarding passes.

**Introduction**

So we have this constantly increasing boarding pass issuing demand.
Considering that everybody in the team is developing something else, I have
 decided to solve this by creating a microservice handling all the tickets
 and reservation issuing. The solution is simple and looks basically like this:
 
 ![Flapper Passbook Diagram](/readme_files/flapper_boarding_pass.png)
 
 The result is passbook with Flapper identity:
 
 ![Flapper Passbook Front](/readme_files/boarding_pass_front.png) ![Flapper Passbook Back](/readme_files/boarding_pass_back.png)
 
 **Requirements**
 
 All the python packages are described in requirements.txt:
 * Flask;
 * jsonpickle;
 * jsonschema;
 * boto3;
 * wallet-py3k.
 
 **Usage**
 
 - Store your certificates in certificate folder;
 - Define all the parameters in config.py;
 - After installing Docker please type the following command inside the project folder:
  `docker-compose up --build`.
  
  Note: Flapper logo and name are property of Flapper Tecnologia SA. 
