# Flapper Passbook
Microservice that generates Flapper boarding passes.

**Introduction**

So we have this constantly increasing boarding pass issuing demand.
Considering that everybody in the team is developing something else, I have to
 decided to solve this creating a microservice handling all the tickets
 and reservation issuing. The solution is simple and looks basically like this:
 
 ![Flapper Passbook Diagram](/readme_files/flapper_passbook.png)
 
 The result is passbook with Flapper identity:
 
 ![Flapper Passbook Front](/readme_files/passbook_front.png) ![Flapper Passbook Back](/readme_files/passbook_back.png)
 
 **Requirements**
 
 Docker all the python packages are described in requirements.txt
 
 **Usage**
 
 Just after installing Docker type the following command inside the project folder:
  `docker-compose up --build`
