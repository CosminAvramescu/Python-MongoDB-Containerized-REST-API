<!-- PROJECT LOGO -->
<br />
<div align="center">
  <p align="center">
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
# ABOUT THE PROJECT
![api](https://i.imgur.com/QlTdmU0.png)

---Architecture

	    As seen in docker-compose.yml, I have 3 microservices (python-rest-api, MongoDB database and 
    mongo express database utility). I have used 2 networks, one between rest api and mongo db and 
    one between mongo db and mongo express. Both mongo db
    and mongo express are protected by user and password authentication, credentials are found in 
    docker compose. I also used 2 volumes, one for mongo db and one for mongo express. At
    running docker-compose, the database is initialized with the init-db.js script (create the 3
    collections - country, city and temperatures and set for each unique constraints on the fields). 
	In Dockerfile I install the packages from requirments.txt, set the current directory, host
    and the port on which the application runs. In docker-compose.yml, I drag the mongo db and mongo 
    images express, put the credentials in environment variables, and set the ports and volumes for
    data persistence. Build the api from dockerfile.

---General aspects

	    Since MongoDB puts by default a "_id" field of type ObjectID(), the following operations were
    executed several times: update json with "id" instead of "_id" or vice versa and convert from 
    ObjectID() to string to serialize the object and return the response. 
	Besides checking all error cases I could think of, there are insert_one() operations for 
    adding, find_one() for find element, find() for finding all elements, update_one() for put and 
    delete_one() for delete. All these methods in pymongo can receive a json as query parameter. For 
    more complicated queries, I used the syntax "$in": cities, to set the search according to the ids 
    in the previously constructed city array, and for the timestamp we used "$lte" to set the date 
    search lower than until and "$gte" to set the date search higher than from. 


### Built With
* [![Cpp][Cpp]][Cpp-url]



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/CosminAvramescu/Cpp-RPC-Oauth.git
   ```
2. Install rpcgen
   ```sh
   sudo apt-get update
   sudo apt-get install rpcgen

   rpcgen app.x
   sudo rpcbind
   ```


<!-- USAGE EXAMPLES -->
## Usage

1. Run make command.
2. Run ./app_server in a terminal and ./app_client in another terminal. 
3. Run the script ./check.sh to test the app with the tests suite.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Cosmin-Alexandru Avramescu - [@my_linkedin](https://www.linkedin.com/in/cosmin-avramescu/)

Project Link: [https://github.com/CosminAvramescu/Cpp-RPC-Oauth](https://github.com/CosminAvramescu/Cpp-RPC-Oauth)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [rpcgen](https://docs.oracle.com/cd/E19683-01/816-1435/rpcgenpguide-21470/index.html)
* [Oauth](https://www.soapui.org/docs/oauth1/oauth1-overview/)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Cpp]: https://img.shields.io/badge/-C++-blue?logo=cplusplus
[Cpp-url]: https://isocpp.org/
